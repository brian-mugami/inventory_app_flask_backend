from invapp.db import db
from datetime import datetime
class ExpensesModel(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=True, default=0.00)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    update_date = db.Column(db.DateTime)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id", ondelete='SET NULL'), nullable=True)
    lot_id = db.Column(db.Integer, db.ForeignKey("lots.id", ondelete="SET NULL"), nullable=True)

    lot = db.relationship("LotModel", back_populates="expense_item")
    item = db.relationship("ItemModel", back_populates="expense_item")
    invoice = db.relationship("InvoiceModel", back_populates="expense_item")

    __table_args__ = (
        db.UniqueConstraint('item_id', 'invoice_id'),
    )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

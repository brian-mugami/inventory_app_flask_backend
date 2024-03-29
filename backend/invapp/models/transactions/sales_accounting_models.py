import uuid

from invapp.db import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class SalesAccountingModel(db.Model):
    __tablename__ = "sales_accounting"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    credit_amount = db.Column(db.Float,default=0.000)
    debit_amount = db.Column(db.Float,default=0.000)
    update_date = db.Column(db.DateTime)
    accounting_status = db.Column(db.Enum("account","void", name="accounting_rules"), default="account")
    credit_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id", ondelete='SET NULL'))
    debit_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id", ondelete='SET NULL'))

    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.id", ondelete='CASCADE'))
    receipt = db.relationship("ReceiptModel", back_populates="accounting")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()


class CustomerPayAccountingModel(db.Model):
    __tablename__ = "customer_payment_accounting"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    credit_amount = db.Column(db.Float,default=0.000)
    debit_amount = db.Column(db.Float,default=0.000)
    update_date = db.Column(db.DateTime)
    credit_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id", ondelete='SET NULL'))
    debit_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id", ondelete='SET NULL'))

    payment_id = db.Column(db.Integer, db.ForeignKey("customer_payments.id", ondelete="CASCADE"), nullable=False)
    balance_id = db.Column(db.Integer, db.ForeignKey("customer_balances.id",ondelete="CASCADE"), nullable=False)

    payments = db.relationship("CustomerPaymentModel", back_populates="accounting")
    balance = db.relationship("CustomerBalanceModel", back_populates="accounting")


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()
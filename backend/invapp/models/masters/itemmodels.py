from invapp.db import db
from datetime import datetime, timedelta


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    item_image = db.Column(db.String(50), nullable=False, default="item.png")
    item_name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    item_number = db.Column(db.Integer, db.Sequence(__tablename__ + "_id_seq", start=100, increment=2), index=True,
                            unique=True)
    item_unit = db.Column(db.Float, default=0.0)
    unit_type = db.Column(
        db.Enum('unit', 'g', 'Kg', 'mg', 'L', 'ml', 'M', 'cm', 'mm', 'inch', 'feet', 'tonnes', 'm3', 'm2', 'cm2',
                name='item_unit_types'), nullable=True, default='unit')
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_archived = db.Column(db.DateTime)
    is_archived = db.Column(db.Boolean, default=False)
    date_unarchived = db.Column(db.DateTime)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False, default=1.00)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    category = db.relationship("CategoryModel", back_populates="items")
    purchase = db.relationship("PurchaseModel", back_populates="item", lazy="dynamic")
    inventory_item = db.relationship("InventoryBalancesModel", back_populates="item", lazy="dynamic")
    sales = db.relationship("SalesModel", back_populates="item", lazy="dynamic")
    expense_item = db.relationship("ExpensesModel", back_populates="item", lazy="dynamic")

    def deactivate_item(self):
        self.is_active = False
        self.is_archived = True
        self.date_archived = datetime.utcnow()

        db.session.commit(self)

    def activate_item(self):
        self.is_active = True
        self.is_archived = False
        self.date_archived = None
        self.date_unarchived = datetime.utcnow()
        db.session.commit(self)

    def deactivate_account(self):
        self.is_active = False
        self.is_archived = True
        self.date_archived = datetime.utcnow()

        db.session.commit(self)

    def activate_account(self):
        self.is_active = True
        self.is_archived = False
        self.date_archived = None
        self.date_unarchived = datetime.utcnow()
        db.session.commit(self)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()


class LotModel(db.Model):
    __tablename__ = "lots"
    id = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.String(50), nullable=False, unique=True)
    lot = db.Column(db.String(50), nullable=False, unique=True)
    expiry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + timedelta(days=256))
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_unarchived = db.Column(db.DateTime)
    date_archived = db.Column(db.DateTime)
    is_archived = db.Column(db.Boolean, default=False)

    expense_item = db.relationship("ExpensesModel", back_populates="lot")
    invoice_item = db.relationship("PurchaseModel", back_populates="lot")
    inventory_item = db.relationship("InventoryBalancesModel", back_populates="lot")

    def deactivate_lot(self):
        self.is_active = False
        self.is_archived = True
        self.date_archived = datetime.utcnow()

        db.session.commit(self)

    def activate_lot(self):
        self.is_active = True
        self.is_archived = False
        self.date_archived = None
        self.date_unarchived = datetime.utcnow()
        db.session.commit(self)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_archived = db.Column(db.DateTime)
    is_archived = db.Column(db.Boolean, default=False)
    date_unarchived = db.Column(db.DateTime)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, unique=True)

    items = db.relationship("ItemModel", back_populates="category", lazy="dynamic")
    account = db.relationship("AccountModel", back_populates="category")

    def deactivate_category(self):
        self.is_active = False
        self.is_archived = True
        self.date_archived = datetime.utcnow()

        db.session.commit(self)

    def activate_category(self):
        self.is_active = True
        self.is_archived = False
        self.date_archived = None
        self.date_unarchived = datetime.utcnow()
        db.session.commit(self)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

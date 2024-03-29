from marshmallow import Schema, fields

from .supplierschema import SupplierSchema
from .itemschema import PlainItemSchema


class Invoice(Schema):
    id = fields.Int(required=True)
    supplier = fields.Nested(SupplierSchema(), dump_only=True)
    invoice_number = fields.String()
    amount = fields.Float(dump_only=True, required=True)
    matched_to_lines = fields.String(required=True, dump_only=True)


class LotSchema(Schema):
    id = fields.Int(dump_only=True)
    batch = fields.String()
    lot = fields.String()
    expiry_date = fields.Date()


class PurchaseItemSchema(Schema):
    item_id = fields.Int(required=True, dump_only=True)
    item_name = fields.String(required=True)
    buying_price = fields.Float(required=True)
    lot_id = fields.Int(required=False, dump_only=True)
    lot = fields.String(required=False)
    item_quantity = fields.Int(required=True)
    item_cost = fields.Float(dump_only=True, required=True)


class PlainPurchasingSchema(Schema):
    id = fields.Int(dump_only=True, required=True)
    items_list = fields.List(fields.Nested(PurchaseItemSchema(), required=True))
    invoice_id = fields.Int(required=True)
    invoice_amount = fields.Float(required=True, dump_only=True)


class PurchasingSchema(PlainPurchasingSchema):
    items = fields.Nested(PlainItemSchema(), dump_only=True)
    invoice = fields.Nested(Invoice(), dump_only=True)
    lot = fields.Nested(LotSchema(), dump_only=True)


class PlainPurchaseUpdateSchema(Schema):
    item_id = fields.Int(dump_only=True)
    item_name = fields.String()
    buying_price = fields.Float()
    quantity = fields.Int()
    lot_id = fields.Int(dump_only=True)
    lot = fields.String()
    item_cost = fields.Float(dump_only=True)


class PurchaseUpdateSchema(Schema):
    item_list = fields.List(fields.Nested(PlainPurchaseUpdateSchema()))
    invoice_id = fields.Int()
    invoice = fields.Nested(Invoice(), dump_only=True)
    lot = fields.Nested(LotSchema(), dump_only=True)

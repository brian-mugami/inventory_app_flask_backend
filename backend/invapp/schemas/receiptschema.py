import datetime
from marshmallow import fields, Schema, validate

from ..schemas.itemschema import PlainItemSchema

class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_name = fields.Str()
class ReceiptPaginationSchema(Schema):
    page = fields.Int(default=1)
    per_page = fields.Int(default=50)

class BalanceSchema(Schema):
    id = fields.Int()
    paid = fields.Float()
    balance = fields.Float()

class ReceiptItems(Schema):
    id = fields.Int(required=True, dump_only=True)
    item_id = fields.Int()
    quantity = fields.Int()
    selling_price = fields.Float()
    item_cost = fields.Float()
    item = fields.Nested(PlainItemSchema(), dump_only=True)

class ReceiptSchema(Schema):
    id = fields.Int(dump_only=True)
    transaction_number = fields.UUID(dump_only=True)
    receipt_number = fields.Int(dump_only=True)
    description = fields.Str()
    currency = fields.Str(required=True)
    date = fields.Date(required=True, default=datetime.datetime.utcnow())
    update_date = fields.DateTime(dump_only=True)
    amount = fields.Float()
    sale_type = fields.Str(validate=validate.OneOf(["cash", "credit"]))
    accounted_status = fields.String(validate=validate.OneOf(["fully_accounted", "partially_accounted", "not_accounted"]))
    status = fields.String(validate=validate.OneOf(["fully paid", "partially paid", "not paid", "over paid"]))
    customer_id = fields.Int(required=True, dump_only=True)
    customer_name = fields.String(required=True)
    customer = fields.Nested(CustomerSchema(), dump_only=True)
    sale_items = fields.List(fields.Nested(ReceiptItems(), dump_only=True))
    customer_balance = fields.Nested(BalanceSchema(), dump_only=True, many=True)

class ReceiptPaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    payment_description = fields.String()
    receipt_id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    payment_status = fields.String(dump_only=True)
    currency = fields.Str(required=True)
    receipt_account = fields.String(required=True)
    receive_account_id = fields.Int(dump_only=True, required=True)

    receipt = fields.Nested(ReceiptSchema(), dump_only=True)

class ReceiptVoidSchema(Schema):
    reason = fields.String(required=True)
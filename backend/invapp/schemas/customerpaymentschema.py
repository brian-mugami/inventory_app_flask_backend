from marshmallow import fields,Schema
from .salesschema import SalesSchema

class PlainCustomerPaymentSchema(Schema):

    id = fields.Integer(required=True, dump_only=True)
    transaction_number = fields.UUID(required=True, dump_only=True)
    amount = fields.Float(required=True)
    currency = fields.String(required=True)
    date = fields.Date(dump_only=True)
    payment_status = fields.String(dump_only=True, required=True)
    update_date = fields.Date()
    receive_account_id = fields.Int(required=True)
    sale_id= fields.Int(required=True)
    approved = fields.Boolean(required=True, dump_only=True)

    sale = fields.Nested(SalesSchema(), dump_only=True)

class PaymentUpdateSchema(Schema):
    amount = fields.Float()
    receive_account_id = fields.Int()
    sale_id = fields.Int()
    approved = fields.Boolean()
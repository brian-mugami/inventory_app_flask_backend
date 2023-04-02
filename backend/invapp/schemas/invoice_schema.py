from marshmallow import Schema, fields, validate


class SupplierSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    supplier_name = fields.String()

class Purchase_items(Schema):
    item_quantity = fields.Integer()
    buying_price =  fields.Float()
    item_cost = fields.Float()
    item_id = fields.Int()


class InvoiceSchema(Schema):
    id = fields.Integer(dump_only=True)
    transaction_number = fields.UUID(dump_only=True)
    invoice_number = fields.String(required=True, validate=validate.Length(max=256))
    description = fields.String(validate=validate.Length(max=256))
    currency = fields.String(required=True, validate=validate.Length(max=10))
    amount = fields.Float(required=True)
    date = fields.DateTime()
    destination_type = fields.String(validate=validate.OneOf(["expense", "stores"]))
    purchase_type = fields.String(validate=validate.OneOf(["cash", "credit"]))
    update_date = fields.DateTime()
    supplier_id = fields.Integer(required=True)
    supplier = fields.Nested(SupplierSchema(), dump_only=True)
    purchase_items = fields.List(fields.Nested(Purchase_items(), many=True), dump_only=True)
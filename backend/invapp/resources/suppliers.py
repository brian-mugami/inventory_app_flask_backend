from flask import jsonify
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from ..db import db
from ..models.masters import AccountModel
from ..models.masters.suppliermodels import SupplierModel
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint,abort
from ..schemas.accountsschema import AccountSchema, AccountUpdateSchema
from ..schemas.supplierschema import SupplierSchema

blp = Blueprint("Suppliers", __name__, description="Operations on suppliers")

@blp.route("/supplier/account")
class SupplierAccount(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, data):
        account = AccountModel.query.filter_by(
            account_name=data["account_name"],
            account_category= "Supplier Account"
        ).first()
        if account:
            abort(409, message="Account already exists")

        account = AccountModel(account_name=data["account_name"], account_number=data["account_number"],
                               account_description=data["account_description"], account_category="Supplier Account")

        db.session.add(account)
        db.session.commit()
        return account
    @jwt_required(fresh=False)
    @blp.response(201, AccountSchema(many=True))
    def get(self):
        accounts = AccountModel.query.filter_by(account_category="Supplier Account").all()
        return accounts

@blp.route("/supplier/account/<int:id>")
class SupplierAccountView(MethodView):
    @jwt_required(fresh=True)
    @blp.response(204, AccountSchema)
    def delete(self, id):
        account = AccountModel.query.get_or_404(id)
        if account.account_category != "Supplier Account":
            abort(400, message="This is not an supplier account")
        db.session.delete(account)
        db.session.commit()

        return account

    @jwt_required(fresh=True)
    @blp.response(202, AccountSchema)
    def get(self, id):
        account = AccountModel.query.get_or_404(id)
        if account.account_category != "Supplier Account":
            abort(400, message="This is not a supplier account")
        return account

    @jwt_required(fresh=True)

    @blp.arguments(AccountUpdateSchema)
    def patch(self, data, id):
        account = AccountModel.query.get_or_404(id)
        if account.account_category != "Supplier Account":
            abort(400, message="This is not a supplier account")
        account.account_name = data["account_name"]
        account.account_description = data["account_description"]
        account.account_number = data["account_number"]
        db.session.commit()
        return jsonify({"message": "account updated"}), 202

@blp.route("/supplier")
class Supplier(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(SupplierSchema)
    @blp.response(201, SupplierSchema)
    def post(self, data):
        supplier = SupplierModel.query.filter_by(supplier_name=data["supplier_name"]).first()
        if supplier:
            abort(409, message=f"Supplier {data.get('supplier_name')} already exists")
        account = AccountModel.query.filter_by(
            account_name=data["account_name"],
            account_category="Supplier Account"
        ).first()
        if account is None:
            abort(404, message="Account does not exist")
        account_id = account.id
        data.pop("account_name")
        try:
            supplier = SupplierModel(**data, account_id=account_id)
            db.session.add(supplier)
            db.session.commit()
            return supplier
        except IntegrityError:
            abort(500, message="Please review the creation details, there was an error")

    @jwt_required(fresh=False)
    @blp.response(200, SupplierSchema(many=True))
    def get(self):
        suppliers = SupplierModel.query.all()
        return suppliers

@blp.route("/supplier/<int:id>")
class SupplierView(MethodView):
    @jwt_required(fresh=True)
    @blp.response(202, SupplierSchema)
    def delete(self, id):
        supplier = SupplierModel.query.get_or_404(id)
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({"message": "supplier deleted"}), 204

    @jwt_required(fresh=True)
    @blp.response(202, SupplierSchema)
    def get(self, id):
        supplier = SupplierModel.query.get_or_404(id)

        return supplier

    @jwt_required(fresh=True)
    @blp.arguments(SupplierSchema)
    @blp.response(201, SupplierSchema)
    def patch(self, data, id):
        supplier = SupplierModel.query.get_or_404(id)
        if supplier:
            supplier.supplier_name = data["supplier_name"]
            supplier.supplier_phone_no = data["supplier_phone_no"]
            supplier.supplier_email = data["supplier_email"]
            supplier.supplier_site = data["supplier_site"]
            supplier.is_active = data["is_active"]

            supplier_account = AccountModel.query.filter_by(
                account_name=data["account_name"],
                account_category="Supplier Account"
            ).first()
            if supplier_account is None:
                abort(404, message="Account does not exist")

            supplier.account_id = supplier_account.id

            db.session.commit()

@blp.route("/supplier/count")
class SupplierCount(MethodView):
    @jwt_required(fresh=True)
    def get(self):
        suppliers = db.session.execute(SupplierModel.query.filter_by(is_active=True).statement.with_only_columns(func.count()).order_by(None)).scalar()
        #suppliers = db.session.execute('select count(id) as c from suppliers where is_active= true').scalar()
        return jsonify({"suppliers": suppliers}), 202

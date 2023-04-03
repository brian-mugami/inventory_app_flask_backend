import datetime
from typing import List

from blinker import signal

from invapp.models.transactions.inventory_balances import InventoryBalancesModel
from invapp.models.transactions.purchase_accounting_models import PurchaseAccountingModel, SupplierPayAccountingModel
from invapp.models.transactions.supplier_balances_model import SupplierBalanceModel
from invapp.models.transactions.customer_balances_model import CustomerBalanceModel
from invapp.models.transactions.expenses_model import ExpensesModel
from flask import jsonify
from invapp.models.transactions.sales_accounting_models import SalesAccountingModel, CustomerPayAccountingModel

send_data = signal('send-data')
purchase_account = signal('purchase_account')
pay_supplier = signal("pay-supplier")
supplier_balance = signal("supplier_balance")
sales_account = signal("sales_account")
customer_balance = signal("customer_balance")
customer_payment = signal("customer_payment")
expense_addition = signal("signal_addition")


class SignalException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

@expense_addition.connect
def expense_addition(items: List,purchase_id:int,date: str=None):
    for item in items:
        item = ExpensesModel.query.filter_by(purchase_id=purchase_id, item_id=item["id"]).first()
        if item:
            item.unit_cost = item["buying_price"]
            item.quantity = item["quantity"]
            item.update_date = datetime.datetime.utcnow()
            item.update_db()
            return item.id
        onhand_item = ExpensesModel(item_id=item["id"], purchase_id=purchase_id,unit_cost=item["buying_price"], quantity=item["quantity"], date=date)
        try:
            onhand_item.save_to_db()
            return onhand_item.id
        except:
            raise SignalException("Failed to add to expense")

@send_data.connect
def increase_stock_addition(items: List,purchase_id:int, date: str=None):
    for item in items:
        item = InventoryBalancesModel.query.filter_by(purchase_id=purchase_id, item_id=item["id"]).first()
        if item:
            item.unit_cost = item["buying_price"]
            item.quantity = item["quantity"]
            item.update_date = datetime.datetime.utcnow()
            item.update_db()
            return item.id
        onhand_item = InventoryBalancesModel(item_id=item["id"], purchase_id=purchase_id,unit_cost=item["buying_price"], quantity=item["quantity"], date=date)
        try:
            onhand_item.save_to_db()
            return onhand_item.id
        except:
            raise SignalException("Failed to add to stores")


@purchase_account.connect
def purchase_accouting_transaction(purchase_account_id: int, purchase_id: int,supplier_account_id: int,invoice_amount: float, inv_id: int=None, expense_id: int =None):
    existing_accounting = PurchaseAccountingModel.query.filter_by(purchase_id=purchase_id, inventory_id=inv_id, expense_id=expense_id).first()
    if existing_accounting:
        existing_accounting.credit_account_id = supplier_account_id
        existing_accounting.debit_account_id = purchase_account_id
        existing_accounting.credit_amount = -invoice_amount
        existing_accounting.debit_amount = invoice_amount
        existing_accounting.update_date = datetime.datetime.utcnow()
        existing_accounting.update_db()
        return jsonify({"message": "updated"})
    purchase_account = PurchaseAccountingModel(credit_account_id=supplier_account_id,debit_account_id=purchase_account_id,
                                          debit_amount=invoice_amount, credit_amount=-invoice_amount, purchase_id=purchase_id, inventory_id=inv_id, expense_id=expense_id)
    try:
        purchase_account.save_to_db()
        return jsonify({"added": "success"})
    except:
        raise SignalException("Failed to add to accounts")

@pay_supplier.connect
def make_payement(supplier_account_id: int, credit_account: int, amount: float, payment_id: int, balance_id: int):
    existing = SupplierPayAccountingModel.query.filter_by(payment_id=payment_id, balance_id=balance_id).first()
    if existing:
        existing.update_date = datetime.datetime.utcnow()
        existing.credit_amount = -amount
        existing.debit_amount = amount
        existing.credit_account_id = credit_account
        existing.debit_account_id = supplier_account_id
        existing.update_db()
        return jsonify({"message": "updated"})
    else:
        new_payment = SupplierPayAccountingModel(credit_amount = -amount, debit_amount= amount, credit_account_id= credit_account, debit_account_id=supplier_account_id, payment_id=payment_id, balance_id=balance_id)
        try:
            new_payment.save_to_db()
        except:
            raise SignalException("Payment failed")

@customer_payment.connect
def receive_payment(customer_account_id: int, bank_account: int, amount: float, payment_id: int, balance_id: int):
    existing = CustomerPayAccountingModel.query.filter_by(payment_id=payment_id, balance_id=balance_id).first()
    if existing:
        existing.update_date = datetime.datetime.utcnow()
        existing.credit_amount = -amount
        existing.debit_amount = amount
        existing.credit_account_id = customer_account_id
        existing.debit_account_id = bank_account
        existing.update_db()
        return jsonify({"message": "updated"})
    else:
        new_payment = CustomerPayAccountingModel(credit_amount = -amount, debit_amount= amount, credit_account_id= customer_account_id, debit_account_id=bank_account, payment_id=payment_id, balance_id=balance_id)
        try:
            new_payment.save_to_db()
        except:
            raise SignalException("Payment failed")




@supplier_balance.connect
def add_supplier_balance(supplier_id: int,purchase_id: int,invoice_amount: float , currency: str = "KES", paid: float = 0.00):
    balance = invoice_amount - paid

    existing_balance = SupplierBalanceModel.query.filter_by(supplier_id=supplier_id, currency=currency, purchase_id=purchase_id).first()
    if existing_balance:
        existing_balance.paid += paid
        existing_balance.invoice_amount = invoice_amount
        existing_balance.balance -= paid
        existing_balance.date = datetime.datetime.utcnow()
        existing_balance.update_db()
        return existing_balance.id
    else:
        sup_balance = SupplierBalanceModel(supplier_id=supplier_id, purchase_id=purchase_id, invoice_amount=invoice_amount, paid=paid, balance=balance, currency=currency, date=datetime.datetime.utcnow())
        try:
            sup_balance.save_to_db()
            return sup_balance.id
        except:
            raise SignalException("supplier balance update failed")


@sales_account.connect
def sales_accounting_transaction(sales_account_id: int, sale_id: int,customer_account_id: int, selling_price: float, quantity: int):
    amount = selling_price * quantity
    existing_accounting = SalesAccountingModel.query.filter_by(sale_id=sale_id).first()
    if existing_accounting:
        existing_accounting.credit_account_id = sales_account_id
        existing_accounting.debit_account_id = customer_account_id
        existing_accounting.credit_amount = -amount
        existing_accounting.debit_amount = amount
        existing_accounting.update_date = datetime.datetime.utcnow()
        existing_accounting.update_db()
        return jsonify({"message": "updated"})
    sales_account = SalesAccountingModel(credit_account_id=sales_account_id,debit_account_id=customer_account_id,
                                          debit_amount=amount, credit_amount=-amount, sale_id=sale_id)
    try:
        sales_account.save_to_db()
        return jsonify({"added": "success"})
    except:
        raise SignalException("Failed to add to accounts")


@customer_balance.connect
def add_customer_balance(customer_id: int,sale_id: int,receipt_amount: float , currency: str = "KES", paid: float = 0.00):
    balance = receipt_amount - paid

    existing_balance = CustomerBalanceModel.query.filter_by(customer_id=customer_id, currency=currency,
                                                            sale_id=sale_id).first()
    if existing_balance:
        existing_balance.paid += paid
        existing_balance.invoice_amount = receipt_amount
        existing_balance.balance -= paid
        existing_balance.date = datetime.datetime.utcnow()
        existing_balance.update_db()
        return existing_balance.id
    else:
        sup_balance = CustomerBalanceModel(customer_id=customer_id, sale_id=sale_id,
                                           receipt_amount=receipt_amount, paid=paid, balance=balance, currency=currency,
                                           date=datetime.datetime.utcnow())
        try:
            sup_balance.save_to_db()
            return sup_balance.id
        except:
            raise SignalException("supplier balance update failed")



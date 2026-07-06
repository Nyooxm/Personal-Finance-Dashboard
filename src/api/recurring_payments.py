#Draft for recurring payments.
#This file will handle the recurring payments feature of the Personal Finance Dashboard.

#Endpoints:
    #GET  /api/recurring_payments        -> returns the list of all recurring payments
    #POST /api/recurring_payments        -> creates a new recurring payment
    #DELETE /api/recurring_payments/<id> -> deletes a recurring payment

#Import the tools required to build the routes, database, etc.
#Create a blueprint named "recurring_payments".

from flask import Blueprint, jsonify, request

recurring_payments_bp = Blueprint('recurring_payments', __name__, url_prefix='/api/recurring_payments')

_recurring_payments = []
_next_id = 1

def get_recurring_payments():
    """Return all recurring payments."""
    return _recurring_payments

def _normalize(payment):
    """Trim whitespace from the payment name."""
    return payment.strip()

def _validate_payment(payment):
    """Check if the payment has the required fields."""
    required_fields = ['name', 'amount', 'category', "due_date"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return f"Missing required fields: {', '.join(missing)}"
    if not _normalize(data['name']):
        return "Payment name cannot be empty."
    if data['amount'] <= 0:
        return "Payment amount must be greater than zero."
    if not (1 <= data ["due_date"].day <= 31 and 1 <= data["due_date"].month <= 12):
        return "Due date must be a valid date."
    
    return None
    
def add_recurring payment(data):
    global _next_id

    error = _validate_payment(data)
    if error:
        return None, error

    payment = {
        "id": _next_id,
        "name": _normalize(data["name"]),
        "amount": data["amount"],
        "category": data["category"],
        "due_day": data["due_day"],
    }

    _recurring_payments.append(payment)
    _next_id += 1

    return payment, None


def delete_recurring_payment(payment_id):
    """
    Delete a recurring payment if it exists.

    Returns True if a payment was deleted, False if it wasn't found.
    """
    match = next((p for p in _recurring_payments if p["id"] == payment_id), None)

    if match is None:
        return False

    _recurring_payments.remove(match)
    return True
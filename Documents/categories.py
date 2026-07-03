#just draft code rn
"""
categories.py

Handles the "categories" feature of the Personal Finance Dashboard.

Endpoints:
    GET  /api/categories        -> returns the list of all categories
    POST /api/categories        -> creates a new category (expects {"name": "..."})
    DELETE /api/categories/<name> -> deletes an existing category

This module uses a simple in-memory store so it can be dropped into any
Flask app and tested immediately. Swap `_categories` for a real database
table later without changing the route logic much.
"""

from flask import Blueprint, jsonify, request

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")

# A reasonable set of general categories to start the user off with.
# Users can add their own on top of these (feature 1: "customizable categories").
DEFAULT_CATEGORIES = [
    "Food",
    "Rent",
    "Utilities",
    "Subscriptions",
    "Transportation",
    "Entertainment",
    "Health",
    "Shopping",
    "Savings",
    "Other",
]

# In-memory "database". Stored as a set internally to make duplicate
# checks trivial, but we always return it to the frontend as a sorted list.
_categories = set(DEFAULT_CATEGORIES)


def get_categories():
    """Return all categories, sorted alphabetically."""
    return sorted(_categories)


def _normalize(name):
    """Trim whitespace so 'Food' and ' Food ' are treated as the same category."""
    return name.strip()


def category_exists(name):
    """Case-insensitive check for whether a category already exists."""
    normalized = _normalize(name).lower()
    return any(normalized == existing.lower() for existing in _categories)


def add_category(name):
    """
    Add a new category if it doesn't already exist.

    Returns a tuple: (category_name_or_None, error_message_or_None)
    """
    name = _normalize(name)

    if not name:
        return None, "Category name cannot be empty."

    if category_exists(name):
        return None, f"Category '{name}' already exists."

    _categories.add(name)
    return name, None


def delete_category(name):
    """
    Delete a category if it exists.

    Returns True if a category was deleted, False if it wasn't found.
    """
    normalized = _normalize(name).lower()
    match = next((c for c in _categories if c.lower() == normalized), None)

    if match is None:
        return False

    _categories.remove(match)
    return True


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@categories_bp.route("", methods=["GET"])
def list_categories():
    """GET /api/categories -> { "categories": [...] }"""
    return jsonify({"categories": get_categories()}), 200


@categories_bp.route("", methods=["POST"])
def create_category():
    """
    POST /api/categories
    Body: { "name": "Groceries" }

    Returns 201 if created, 409 if it already exists, 400 if invalid.
    """
    data = request.get_json(silent=True) or {}
    name = data.get("name", "")

    created_name, error = add_category(name)

    if error:
        status_code = 409 if "already exists" in error else 400
        return jsonify({"error": error}), status_code

    return jsonify({"category": created_name}), 201


@categories_bp.route("/<string:name>", methods=["DELETE"])
def remove_category(name):
    """DELETE /api/categories/<name> -> 200 if deleted, 404 if not found."""
    deleted = delete_category(name)

    if not deleted:
        return jsonify({"error": f"Category '{name}' not found."}), 404

    return jsonify({"message": f"Category '{name}' deleted."}), 200

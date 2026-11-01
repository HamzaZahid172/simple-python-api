"""Small, testable Flask API with an in-memory item store."""

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

SEED_ITEMS = (
    {"id": 1, "name": "Python Basics", "category": "course"},
    {"id": 2, "name": "API Development", "category": "course"},
)


def create_app():
    """Create an isolated app for development and tests."""
    app = Flask(__name__)
    app.config["ITEMS"] = [item.copy() for item in SEED_ITEMS]
    app.config["NEXT_ITEM_ID"] = max(item["id"] for item in SEED_ITEMS) + 1

    @app.get("/")
    def home():
        return jsonify({
            "message": "Welcome to the Simple Python API",
            "endpoints": ["/health", "/items", "/items/<id>", "DELETE /items/<id>", "/add-item"],
        })

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "simple-python-api"})

    @app.get("/items")
    def get_items():
        category = request.args.get("category")
        items = app.config["ITEMS"]
        if category is not None:
            items = [item for item in items if item["category"] == category]

        # Preserve the existing response for callers not requesting pagination.
        raw_limit = request.args.get("limit")
        raw_offset = request.args.get("offset")
        if raw_limit is None and raw_offset is None:
            return jsonify({"items": items, "count": len(items)})

        # Bound the numeric input before converting to an int.
        def is_valid_number(value):
            return value.isascii() and value.isdigit() and len(value) <= 9

        if raw_limit is not None and (
            not is_valid_number(raw_limit) or not 1 <= int(raw_limit) <= 100
        ):
            return jsonify({"error": "limit must be an integer between 1 and 100"}), 400
        if raw_offset is not None and not is_valid_number(raw_offset):
            return jsonify({"error": "offset must be a non-negative integer"}), 400

        limit = int(raw_limit) if raw_limit is not None else 20
        offset = int(raw_offset) if raw_offset is not None else 0
        page = items[offset:offset + limit]
        return jsonify({
            "items": page,
            "count": len(page),
            "total": len(items),
            "offset": offset,
            "limit": limit,
        })

    @app.get("/items/<int:item_id>")
    def get_item(item_id):
        item = next((item for item in app.config["ITEMS"] if item["id"] == item_id), None)
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item)

    @app.delete("/items/<int:item_id>")
    def delete_item(item_id):
        items = app.config["ITEMS"]
        for index, item in enumerate(items):
            if item["id"] == item_id:
                items.pop(index)
                return "", 204
        return jsonify({"error": "Item not found"}), 404

    @app.post("/add-item")
    def add_item():
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify({"error": "Malformed JSON body"}), 400
        if not isinstance(data, dict):
            return jsonify({"error": "Expected a JSON object"}), 400

        name, category = data.get("name"), data.get("category")
        if any(not isinstance(value, str) or not value.strip() for value in (name, category)):
            return jsonify({"error": "name and category must be non-empty strings"}), 400
        name, category = name.strip(), category.strip()
        if len(name) > 100 or len(category) > 100:
            return jsonify({"error": "name and category must be at most 100 characters"}), 400

        items = app.config["ITEMS"]
        next_id = app.config["NEXT_ITEM_ID"]
        app.config["NEXT_ITEM_ID"] += 1
        new_item = {"id": next_id, "name": name, "category": category}
        items.append(new_item)
        return jsonify({"message": "Item added successfully", "item": new_item}), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)

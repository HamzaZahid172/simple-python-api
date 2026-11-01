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

    @app.get("/")
    def home():
        return jsonify({
            "message": "Welcome to the Simple Python API",
            "endpoints": ["/health", "/items", "/items/<id>", "/add-item"],
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
        return jsonify({"items": items, "count": len(items)})

    @app.get("/items/<int:item_id>")
    def get_item(item_id):
        item = next((item for item in app.config["ITEMS"] if item["id"] == item_id), None)
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item)

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
        next_id = max((item["id"] for item in items), default=0) + 1
        new_item = {"id": next_id, "name": name, "category": category}
        items.append(new_item)
        return jsonify({"message": "Item added successfully", "item": new_item}), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)

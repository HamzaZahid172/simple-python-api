from flask import Flask, jsonify, request

app = Flask(__name__)


items = [
    {"id": 1, "name": "Python Basics", "category": "course"},
    {"id": 2, "name": "API Development", "category": "course"},
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Simple Python API",
        "endpoints": ["/health", "/items", "/items/<id>", "/add-item"]
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "simple-python-api"})

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": items, "count": len(items)})

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.route("/add-item", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or "name" not in data or "category" not in data:
        return jsonify({"error": "Please provide name and category"}), 400

    new_item = {
        "id": len(items) + 1,
        "name": data["name"],
        "category": data["category"],
    }
    items.append(new_item)
    return jsonify({"message": "Item added successfully", "item": new_item}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ เปิด CORS ครอบคลุมทุก method
CORS(app, resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# ---------------------------
# DATA MOCK (เก็บใน memory)
# ---------------------------
todos = [
    {"id": 1, "title": "เขียนรายงาน Flask CI/CD", "description": "ส่งอาจารย์ Pongkiat", "done": False},
    {"id": 2, "title": "ออกแบบหน้า Next.js", "description": "Todo list frontend", "done": True},
    {"id": 3, "title": "อ่านหนังสือสอบ Use of English", "description": "Section 1 & 2", "done": False},
]
next_id = 4


# ---------------------------
# ROUTES
# ---------------------------

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(todos), 200


@app.route("/api/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json()
    new_todo = {
        "id": next_id,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "done": False
    }
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json(force=True)
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = data.get("done", todo["done"])
            todo["title"] = data.get("title", todo["title"])
            todo["description"] = data.get("description", todo["description"])
            return jsonify(todo), 200
    return jsonify({"error": "Not found"}), 404


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"deleted": todo_id}), 200


@app.route("/")
def home():
    return jsonify({"message": "Flask Todo API is running!"}), 200


# ---------------------------
# MAIN ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

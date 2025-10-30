from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ ปรับ CORS ให้รองรับทุกอย่างชัดเจน
CORS(app, resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# ---------------------------
# ROUTES
# ---------------------------
@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/api/todos", methods=["GET"])
def get_todos():
    todos = [
        {"id": 1, "title": "เขียนรายงาน Flask CI/CD", "description": "ส่งอาจารย์ Pongkiat", "done": False},
        {"id": 2, "title": "ออกแบบหน้า Next.js", "description": "Todo list frontend", "done": True},
        {"id": 3, "title": "อ่านหนังสือสอบ Use of English", "description": "Section 1 & 2", "done": False},
    ]
    return jsonify(todos), 200

@app.route("/api/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    new_todo = {
        "id": 999,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "done": False
    }
    return jsonify(new_todo), 201

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    return jsonify({"deleted": todo_id}), 200

@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    return jsonify({"updated": todo_id, "data": data}), 200

@app.route("/")
def home():
    return jsonify({"message": "Flask Todo API is running!"}), 200

# ---------------------------
# MAIN ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

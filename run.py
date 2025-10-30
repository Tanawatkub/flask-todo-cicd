from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ เปิดอนุญาตทุก origin ที่จำเป็น
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://tanawatputta.github.io",
            "https://*.github.io",
            "https://flask-todo-app-3r5b.onrender.com"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ---------------------------
# ✅ ROUTES
# ---------------------------

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/todos", methods=["GET"])
def get_todos():
    """ส่ง mock data กลับให้ frontend"""
    todos = [
        {"id": 1, "title": "เขียนรายงาน Flask CI/CD", "description": "ส่งอาจารย์ Pongkiat", "done": False},
        {"id": 2, "title": "ออกแบบหน้า Next.js", "description": "Todo list frontend", "done": True},
        {"id": 3, "title": "อ่านหนังสือสอบ Use of English", "description": "Section 1 & 2", "done": False},
    ]
    return jsonify(todos), 200


@app.route("/api/todos", methods=["POST"])
def create_todo():
    """รับข้อมูลจาก frontend แล้วส่งกลับ mock id"""
    data = request.get_json()
    new_todo = {
        "id": 999,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "done": False
    }
    return jsonify(new_todo), 201


@app.route("/")
def home():
    return jsonify({"message": "Flask Todo API is running!"}), 200


# ---------------------------
# ✅ MAIN ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

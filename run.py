from flask import Flask, jsonify
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

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/")
def home():
    return jsonify({"message": "Flask Todo API is running!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

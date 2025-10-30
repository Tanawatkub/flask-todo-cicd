import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/")
def home():
    return jsonify({"message": "Flask Todo CI/CD is running!"}), 200

if __name__ == "__main__":
    # ✅ ใช้พอร์ตจาก Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

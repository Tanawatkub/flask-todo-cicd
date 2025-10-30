from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/')
def home():
    return jsonify({"message": "Flask Todo CI/CD is running!"}), 200


if __name__ == "__main__":
    # ✅ ใช้พอร์ตจาก environment variable (Render จะส่งมาให้)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
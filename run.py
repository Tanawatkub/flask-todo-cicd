from app import create_app
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # ← ใช้ PORT จาก Render หรือ 5001 เป็นค่า default
    app.run(host="0.0.0.0", port=port)

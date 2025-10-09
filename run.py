from flask import Flask, jsonify   # ✅ นำเข้า Flask และ jsonify (แปลงข้อมูลเป็น JSON)

app = Flask(__name__)              # ✅ สร้างแอป Flask ชื่อว่า app

@app.route('/api/health')          # ✅ กำหนดเส้นทาง (URL) ให้กับฟังก์ชันนี้
def health():                      # ✅ ฟังก์ชันที่ทำงานเมื่อมีการเรียก /api/health
    return jsonify({"status": "healthy"}), 200   # ✅ ตอบกลับ JSON บอกว่าแอปยังทำงานดี (status 200 = OK)

if __name__ == "__main__":         # ✅ บอกว่าให้รันแอปถ้าไฟล์นี้ถูกรันโดยตรง
    app.run(host="0.0.0.0", port=5000)  # ✅ เปิดให้เข้าถึงจากทุกเครื่อง ผ่านพอร์ต 5000

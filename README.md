📈 Quadratic Explorer (ระบบสำรวจและวิเคราะห์ฟังก์ชันกำลังสอง)

📝 คำอธิบายโปรเจกต์ (Project Description)

เว็บแอปพลิเคชัน Quadratic Explorer ช่วยผู้เรียนและผู้สนใจคณิตศาสตร์วิเคราะห์และทำความเข้าใจพฤติกรรมของฟังก์ชันกำลังสอง (y = ax² + bx + c) แบบมีปฏิสัมพันธ์ (Interactive) โดยเปิดรับค่าสัมประสิทธิ์ a, b, c และช่วงแกน X เพื่อประมวลผลคำนวณพิกัดจุดยอด (Vertex), ดิสครีมิแนนต์ (Δ), แกนสมมติ, เส้นสัมผัส และรากของสมการ (ทั้งจำนวนจริงและจำนวนเชิงซ้อน) พร้อมแสดงผลผ่านกราฟ Matplotlib รูปแบบสมการ LaTeX ตารางพิกัด และเปิดให้ดาวน์โหลดข้อมูลเป็นไฟล์ CSV

🎯 คุณสมบัติหลัก (Features)

Interactive Inputs: ปรับเปลี่ยนค่า a, b, c ผ่าน Slider และ Selectbox Presets ใน Sidebar

Validation Check: ระบบตรวจจับกรณี a = 0 (แจ้งเตือนว่าเป็นฟังก์ชันเชิงเส้น) และกรณี x_min ≥ x_max

Calculus Insights: แสดงอนุพันธ์อันดับ 1 (f'(x)), อนุพันธ์อันดับ 2 (f''(x)) และสมการเส้นสัมผัสกราฟ

Multiple Output Views:

Metrics สรุปจุดสำคัญ

กราฟแสดงพาราโบลาพร้อม Marker จุดสำคัญ

รูปแบบสมการ (Standard Form, Vertex Form, Factored Form)

ตารางพิกัด (x, y) และปุ่มดาวน์โหลดไฟล์ CSV

🚀 วิธีการรันในเครื่อง Local (VS Code)

เปิด Terminal ใน VS Code และเปิดใช้งาน Virtual Environment:

py -m venv .venv
.venv\Scripts\activate.bat


ติดตั้ง Dependencies:

python -m pip install -r requirements.txt


รันแอปพลิเคชัน:

python -m streamlit run app.py


📋 แบบตรวจงานก่อนส่ง (Pre-submission Checklist)

[1] แอปเปิดได้โดยไม่มี Error (ทดสอบ a ≠ 0 และ a = 0)

[2] Widget ทุกตัวมีผลต่อการคำนวณจริง (a, b, c, ขอบเขต x, สวิตช์เปิด/ปิด Marker)

[3] ชื่อหัวข้อและป้ายกำกับเข้าใจได้ง่าย (ภาษาไทยพร้อมสัญลักษณ์ทางคณิตศาสตร์)

[4] กราฟมีชื่อแกนและคำอธิบายที่เหมาะสม (Domain/Range, Legend)

[5] ไม่มี Password, API Key หรือโฟลเดอร์ .venv ใน GitHub

[6] มีไฟล์ requirements.txt ครบถ้วน

[7] สามารถ Deploy บน Streamlit Community Cloud ได้สำเร็จ

# Guitar Chord Web - เว็บค้นหาคอร์ดกีตาร์จากลิงก์ YouTube

![Language](https://img.shields.io/badge/Language-Python-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

เว็บแอปพลิเคชันสำหรับค้นหาคอร์ดกีตาร์ที่ออกแบบมาเพื่อลดความยุ่งยากและขั้นตอนในการค้นหาคอร์ดเพลง ผู้ใช้สามารถกรอกชื่อเพลงหรือวางลิงก์จาก YouTube เพื่อให้ระบบดึงข้อมูล, ประมวลผล, และแสดงเนื้อเพลงพร้อมคอร์ดกีตาร์ในหน้าเดียวโดยอัตโนมัติ



## ✨ ฟีเจอร์หลัก (Features)

- **ค้นหาด้วยชื่อเพลง:** สามารถกรอกชื่อเพลงที่ต้องการเพื่อค้นหาคอร์ดได้โดยตรง.
- **ค้นหาด้วยลิงก์ YouTube:** เพียงแค่วางลิงก์ YouTube ของเพลง ระบบจะดึงชื่อเพลงมาค้นหาให้โดยอัตโนมัติ.
- **แสดงผลในหน้าเดียว:** ลดความซับซ้อนโดยการแสดงทั้งเนื้อเพลงและคอร์ดกีตาร์ในหน้าเดียวกัน.
- **ประมวลผลอัตโนมัติ:** ระบบทำงานเชื่อมต่อกับ API ต่างๆ เพื่อค้นหาและสกัดข้อมูลคอร์ดเพลงมาให้ผู้ใช้.

## 🛠️ เทคโนโลยีที่ใช้ (Technology Stack)

- [cite_start]**Back-end:** Python [cite: 199, 259]
- [cite_start]**Front-end:** HTML5, CSS3 [cite: 194, 222, 233]
- **APIs:**
    - [cite_start]YouTube Data API v3 [cite: 197, 250]
    - [cite_start]Google Custom Search API [cite: 198, 255]
    - [cite_start]Gemini API (สำหรับสกัดข้อมูล) [cite: 196, 245]
- [cite_start]**Deployment:** Firebase Hosting [cite: 195, 240]
- [cite_start]**Development Tools:** Visual Studio Code [cite: 193, 219]

## ⚙️ ขั้นตอนการทำงาน (Workflow)

[cite_start]ระบบมีขั้นตอนการทำงานตามที่ออกแบบไว้ในแผนภาพสถาปัตยกรรมดังนี้[cite: 333]:

1.  **ผู้ใช้ป้อนข้อมูล:** ผู้ใช้กรอกชื่อเพลงหรือวางลิงก์ YouTube ที่หน้าเว็บ (Front-end).
2.  [cite_start]**ดึงข้อมูลชื่อเพลง (ถ้าเป็นลิงก์):** หากผู้ใช้กรอกลิงก์ YouTube ระบบจะเรียกใช้ **YouTube Data API** เพื่อดึงชื่อเพลงจากวิดีโอนั้น[cite: 334].
3.  [cite_start]**ค้นหา URL ของคอร์ด:** ระบบนำชื่อเพลงที่ได้ไปค้นหา URL ของหน้าคอร์ดเพลงผ่าน **Google Custom Search API** ซึ่งตั้งค่าให้ค้นหาเฉพาะในเว็บไซต์เป้าหมาย (Chordzaa)[cite: 336].
4.  [cite_start]**ดึงข้อมูลหน้าเว็บ:** เมื่อได้ URL แล้ว ระบบจะดึงข้อมูลเนื้อหาทั้งหมดของหน้าเว็บนั้น (ในรูปแบบโค้ด HTML)[cite: 338].
5.  [cite_start]**สกัดข้อมูลด้วย AI:** ระบบส่งข้อมูล HTML ทั้งหมดไปให้ **Gemini API** เพื่อทำการวิเคราะห์และสกัดข้อมูลเฉพาะส่วนที่เป็น "เนื้อเพลงและคอร์ดกีตาร์" ออกมาจากส่วนอื่นๆ ที่ไม่เกี่ยวข้อง[cite: 339].
6.  [cite_start]**ส่งผลลัพธ์กลับ:** ระบบนำข้อมูลเนื้อเพลงและคอร์ดที่สะอาดและจัดรูปแบบแล้วส่งกลับไปแสดงผลที่หน้าเว็บให้ผู้ใช้เห็น[cite: 341].

## 🚀 การติดตั้งและใช้งาน (Getting Started)

หากต้องการทดลองรันโปรเจกต์นี้ในเครื่องของคุณ:

1.  **Clone the repository:**
    ```bash
    git clone [https://medium.com/@5735512017/%E0%B8%AA%E0%B8%A3%E0%B8%B8%E0%B8%9B-github-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%88%E0%B8%B3%E0%B9%80%E0%B8%9B%E0%B9%87%E0%B8%99%E0%B8%95%E0%B9%89%E0%B8%AD%E0%B8%87%E0%B8%A3%E0%B8%B9%E0%B9%89-fd0df64cada0](https://medium.com/@5735512017/%E0%B8%AA%E0%B8%A3%E0%B8%B8%E0%B8%9B-github-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%88%E0%B8%B3%E0%B9%80%E0%B8%9B%E0%B9%87%E0%B8%99%E0%B8%95%E0%B9%89%E0%B8%AD%E0%B8%87%E0%B8%A3%E0%B8%B9%E0%B9%89-fd0df64cada0)
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up API Keys:**
    - สร้างไฟล์ `.env` สำหรับเก็บ API Key ของ YouTube, Google Custom Search, และ Gemini
4.  **Run the application:**
    ```bash
    python main.py
    ```

## ⚠️ ข้อจำกัดของระบบ (Limitations)

- [cite_start]ระบบยังพึ่งพาข้อมูลจากเว็บไซต์ Chordzaa เป็นหลัก หากเพลงนั้นไม่มีในเว็บดังกล่าวก็จะไม่สามารถแสดงผลได้[cite: 201].
- [cite_start]ความแม่นยำในการวางตำแหน่งคอร์ดอาจไม่ตรงกับจังหวะจริงของเพลงทั้งหมด[cite: 202].
- [cite_start]รองรับการค้นหาจากลิงก์ของแพลตฟอร์ม YouTube เท่านั้น[cite: 283].

## 👨‍💻 ผู้จัดทำ (Author)

- [cite_start]**นายณภัทร กรดสุวรรณ์** - *มหาวิทยาลัยราชภัฏนครปฐม* [cite: 164, 168]

## 📄 สิทธิ์การใช้งาน (License)

This project is licensed under the MIT License.

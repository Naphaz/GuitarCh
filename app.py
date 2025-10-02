# ก่อนรันโค้ดนี้ ให้ติดตั้งไลบรารีที่จำเป็นทั้งหมดด้วยคำสั่งต่อไปนี้ใน Terminal:
# pip install Flask beautifulsoup4 google-api-python-client google-generativeai requests python-dotenv

from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
import re
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()

# NOTE: For real-world use, store API Keys in environment variables,
# not hard-coded in the source.
# API key definitions
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_KEY = os.getenv("YOUTUBE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

# Configure Gemini and YouTube APIs
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Create a service for Google Custom Search API with the same API key.
search_service = build("customsearch", "v1", developerKey=API_KEY)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_video_id(url):
    """Extracts video ID from a YouTube URL"""
    query = urlparse(url)
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query).get('v', [None])[0]
    return None

def clean_title(title):
    """
    Cleans up the video title to get a more accurate song name for searching.
    It removes common prefixes, suffixes, and metadata found in YouTube titles.
    """
    clean_title = re.sub(r'\(.*?\)|\[.*?\]|ft\..*|feat\..*|official|mv', '', title, flags=re.IGNORECASE)
    clean_title = clean_title.strip()
    if '-' in clean_title:
        clean_title = clean_title.split('-')[0].strip()
    if '|' in clean_title:
        clean_title = clean_title.split('|')[0].strip()

    return clean_title

def get_chord_data(song_title):
    """
    Uses Google Custom Search API to find and fetch chord data from the web.
    Returns both the extracted text context and the URL of the source.
    """
    context = ""
    source_url = None # เพิ่มตัวแปรเพื่อเก็บ URL
    try:
        # ใช้ Google Custom Search API เพื่อค้นหาคอร์ด
        search_query = f"คอร์ดเพลง {song_title}"
        res = search_service.cse().list(
            q=search_query,
            cx=CUSTOM_SEARCH_ENGINE_ID,
            num=5 # ดึงผลลัพธ์ 5 อันดับแรก
        ).execute()
        
        if 'items' in res:
            for item in res['items']:
                # Heuristic to find a good URL to fetch.
                if 'chordzaa' in item['link'].lower(): # เพิ่มเงื่อนไขเพื่อหาเว็บ Chordzaa โดยเฉพาะ
                    url_to_fetch = item['link']
                    break
                elif any(keyword in item['link'].lower() for keyword in ['chord', 'คอร์ด', 'tab']):
                    url_to_fetch = item['link']
                    break
            else: # ถ้าวน loop จบแล้วไม่เจอ Chordzaa ให้ใช้ URL แรกที่เจอก็ได้
                 url_to_fetch = res['items'][0]['link']
            
            # If a good URL is found, fetch the content
            if url_to_fetch:
                print(f"Debug: Found a promising URL. Fetching content from: {url_to_fetch}")
                source_url = url_to_fetch # เก็บ URL ไว้ในตัวแปร
                page_content = requests.get(url_to_fetch, timeout=10).text
                
                if page_content:
                    soup = BeautifulSoup(page_content, 'html.parser')
                    chord_content = soup.find(['pre', 'div'], class_=re.compile('(chord|song-content|lyrics|content|post)'))
                    
                    if chord_content:
                        print(f"Debug: Found chord content on {url_to_fetch}")
                        context = ' '.join(chord_content.get_text().split())[:4000]
                    else:
                        context = ' '.join(soup.get_text().split())[:4000]

    except Exception as e:
        print(f"Debug: An exception occurred during web fetching: {e}")
        
    return context, source_url # ส่งค่า URL กลับมาด้วย

@app.route('/search', methods=['POST'])
def search_song():
    try:
        data = request.json
        youtube_url = data.get('youtube_url')
        song_name = data.get('song_name')
        
        song_title = ""

        if youtube_url:
            video_id = get_video_id(youtube_url)
            if not video_id:
                return jsonify({"result": "URL ไม่ถูกต้องหรือไม่พบ Video ID"}), 400
            
            request_api = youtube.videos().list(part="snippet", id=video_id)
            response_api = request_api.execute()
            
            if not response_api['items']:
                return jsonify({"result": "ไม่พบข้อมูลวิดีโอสำหรับ URL นี้"}), 404

            title = response_api['items'][0]['snippet']['title']
            song_title = clean_title(title)
        elif song_name:
            song_title = song_name
        else:
            return jsonify({"result": "กรุณาใส่ YouTube URL หรือชื่อเพลง"}), 400

        print(f"Debug: Searching for: {song_title}")
        
        # 2. Use the new function to get chord data from the web
        context, source_url = get_chord_data(song_title) # รับค่า URL กลับมาด้วย
        
        if not context:
            return jsonify({"result": f"ขออภัย ฉันไม่สามารถหาข้อมูลคอร์ดเพลง '{song_title}' จากการค้นหาได้"}), 500
        
        print("Debug: Context generated. Now sending to AI.")

        # 3. Send data to the AI with the context from the web
        prompt = f"""
คุณคือผู้เชี่ยวชาญด้านการแกะคอร์ดเพลงและจัดทำแท็บกีตาร์
คำสั่งคือให้สร้างแท็บคอร์ดเพลงสำหรับเพลง "{song_title}" โดยใช้ข้อมูลจากผลลัพธ์การค้นหาที่ให้มาด้านล่างนี้
ถ้าหากข้อมูลที่ได้รับมาขัดแย้งกัน ให้เลือกข้อมูลที่น่าเชื่อถือที่สุด
หากข้อมูลทั้งหมดที่ได้รับมาไม่เพียงพอที่จะสร้างคอร์ดเพลงได้ ให้แจ้งว่า "ไม่พบข้อมูลคอร์ด"

**ข้อมูลที่ใช้ในการอ้างอิง:**
{context}

**รูปแบบการแสดงผลที่ต้องการ:**
- แสดงคอร์ด (Chord) ไว้บนบรรทัดแยกจากเนื้อเพลง และจัดตำแหน่งให้ตรงกับคำร้อง
- แบ่งเนื้อเพลงออกเป็นท่อนๆ อย่างชัดเจน เช่น (Intro), (Verse), (Chorus), (Outro)
- หากมี Capo ให้ระบุตำแหน่งที่เหมาะสม
- หากข้อมูลไม่เพียงพอที่จะสร้างคอร์ดเพลงได้ ให้แสดงข้อความว่า "ไม่พบข้อมูลคอร์ดสำหรับเพลง {song_title}"
"""
        response_ai = model.generate_content(prompt)
        print("Debug: Gemini API response received.")
        # 4. Send the result back to the web page
        result_text = response_ai.text
        if "ไม่พบข้อมูลคอร์ด" in result_text:
             print(f"Debug: Gemini failed to generate chords. Response: {result_text}")
             return jsonify({"result": f"ขออภัย ฉันไม่สามารถหาคอร์ดเพลง '{song_title}' และเนื้อเพลงที่สมบูรณ์ได้ในขณะนี้ กรุณาลองเพลงอื่นอีกครั้ง"}), 500

        # เพิ่มข้อความเครดิตลงในผลลัพธ์
        if source_url:
            result_text += f"\n\nเครดิต: คอร์ดเพลงจาก {source_url}"
            
        print(f"Debug: Chords successfully generated. Length of response: {len(result_text)}")
        return jsonify({"result": result_text})
    except Exception as e:
        print(f"Debug: An exception occurred: {e}")
        return jsonify({"result": f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
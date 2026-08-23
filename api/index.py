from http.server import BaseHTTPRequestHandler
import json
import requests
from groq import Groq

BOT_TOKEN = 'የአዲሱ_ቦትህ_TOKEN_እዚህ_አስገባ'
GROQ_API_KEY = 'የወሰድከው_GROQ_API_KEY_እዚህ_አስገባ'

TELEGRAM_API = f'https://api.telegram.org/bot{BOT_TOKEN}'
client = Groq(api_key=GROQ_API_KEY)

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        'chat_id': chat_id, 
        'text': text, 
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def get_ai_response(user_text):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful, smart AI assistant. Answer accurately in the language the user speaks (Amharic or English)."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "⚠️ ይቅርታ፣ መልሱን ማዘጋጀት አልተቻለም። እባክዎን ትንሽ ቆይተው ድጋሚ ይሞክሩ።"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))

        if "message" in update:
            msg_obj = update["message"]
            chat_id = msg_obj["chat"]["id"]
            text = msg_obj.get("text", "")

            if text == "/start":
                send_message(chat_id, "🤖 **እንኳን ወደ AI ChatGPT ቦት በሰላም መጡ!**\n\nማንኛውንም ጥያቄ በፅሁፍ ይጠይቁኝ፣ ወዲያውኑ እመልስልዎታለሁ።")
            elif text:
                # ከ AI መልስ ጠይቆ ይልካል
                ai_reply = get_ai_response(text)
                send_message(chat_id, ai_reply)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('OK'.encode('utf-8'))
        return

from http.server import BaseHTTPRequestHandler
import json
import requests

BOT_TOKEN = '8950917290:AAErPGnEBGxBBXaehw7Xu_VQNrF8jckMapw'
GROQ_API_KEY = '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'

TELEGRAM_API = f'https://api.telegram.org/bot{BOT_TOKEN}'

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
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful, smart AI assistant. Answer accurately in the language the user speaks (Amharic or English)."},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        data = res.json()
        return data['choices'][0]['message']['content']
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
                ai_reply = get_ai_response(text)
                send_message(chat_id, ai_reply)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('OK'.encode('utf-8'))
        return

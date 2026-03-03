import json
import uuid
import random
import cloudscraper
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
from fake_useragent import UserAgent

app = Flask(__name__)
CORS(app) # Taaki tumhari frontend site se access ho sake
scraper = cloudscraper.create_scraper()
ua = UserAgent(platforms=['mobile'])

# --- CREATOR BYPASS LOGIC ---
CREATOR_INFO = "Mujhe **CRR Group Of Companies** ne banaya hai. Main unka ek advanced AI assistant hoon. 💀🚀"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get("prompt", "")

    # Identity Bypass check
    if any(x in prompt.lower() for x in ["who created you", "kisne banaya", "owner", "creator"]):
        return Response(json.dumps({"text": CREATOR_INFO}), mimetype='application/json')

    def generate():
        url = "https://notegpt.io/api/v2/chat/stream"
        anon_id = str(uuid.uuid4())
        
        headers = {
            'User-Agent': ua.random,
            'Content-Type': 'application/json',
            'X-Forwarded-For': f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            'Origin': 'https://notegpt.io',
            'Referer': 'https://notegpt.io/ai-chat'
        }
        
        cookies = {'anonymous_user_id': anon_id, 'is_accepted_terms': '1'}
        
        payload = {
            "message": prompt,
            "language": "auto",
            "model": "gpt-5-mini",
            "conversation_id": str(uuid.uuid4()),
            "chat_mode": "standard"
        }

        with scraper.post(url, headers=headers, cookies=cookies, json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data: '):
                        try:
                            json_data = json.loads(decoded[6:])
                            text = json_data.get('text', '')
                            if text:
                                yield f"data: {json.dumps({'text': text})}\n\n"
                        except: pass

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)

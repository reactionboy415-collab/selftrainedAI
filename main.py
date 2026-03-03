import json
import uuid
import random
import cloudscraper
from flask import Flask, request, Response
from fake_useragent import UserAgent

app = Flask(__name__)
scraper = cloudscraper.create_scraper()
ua = UserAgent(platforms=['mobile'])

# Creator Identity System
CREATOR_INFO = "Mujhe **CRR Group Of Companies** ne banaya hai. Main unka ek advanced AI assistant hoon. 💀🚀"

@app.route('/api', methods=['GET'])
def chat():
    # p=Prompt parameter read karna
    prompt = request.args.get('p', '')

    if not prompt:
        return {"error": "Bhai, prompt toh dalo! Example: /api?p=Hi"}, 400

    # Branding Check
    if any(x in prompt.lower() for x in ["who created you", "owner", "creator", "kisne banaya"]):
        return Response(CREATOR_INFO, mimetype='text/plain')

    url = "https://notegpt.io/api/v2/chat/stream"
    headers = {
        'User-Agent': ua.random,
        'Content-Type': 'application/json',
        'X-Forwarded-For': f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
        'Origin': 'https://notegpt.io',
        'Referer': 'https://notegpt.io/ai-chat'
    }
    
    cookies = {
        'anonymous_user_id': str(uuid.uuid4()),
        'is_accepted_terms': '1'
    }
    
    payload = {
        "message": prompt,
        "language": "auto",
        "model": "gpt-5-mini",
        "conversation_id": str(uuid.uuid4()),
        "chat_mode": "standard"
    }

    try:
        full_response = ""
        # Streaming response ko collect karke ek baar mein bhej raha hoon
        # kyunki URL parameters usually single string response expect karte hain
        with scraper.post(url, headers=headers, cookies=cookies, json=payload, stream=True, timeout=25) as r:
            for line in r.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data: '):
                        try:
                            json_data = json.loads(decoded[6:])
                            text = json_data.get('text', '')
                            if text:
                                full_response += text
                        except: pass
        
        return Response(full_response, mimetype='text/plain')

    except Exception as e:
        return Response(f"Error: {str(e)}", mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

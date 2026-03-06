import json
import uuid
import random
import cloudscraper
from flask import Flask, request, Response
from flask_cors import CORS
from fake_useragent import UserAgent

app = Flask(__name__)
CORS(app)  # allow browser requests

scraper = cloudscraper.create_scraper()
ua = UserAgent(platforms=['mobile'])

# Creator Identity System
CREATOR_INFO = "Mujhe **CRR Group Of Companies** ne banaya hai. Main unka ek advanced AI assistant hoon. 💀🚀"


@app.route('/api', methods=['GET'])
def chat():

    prompt = request.args.get('p', '')

    if not prompt:
        return {"error": "Prompt required. Example: /api?p=Hi"}, 400

    # branding response
    if any(x in prompt.lower() for x in ["who created you", "owner", "creator", "kisne banaya"]):
        return Response(CREATOR_INFO, mimetype='text/plain')

    url = "https://notegpt.io/api/v2/chat/stream"

    headers = {
        "User-Agent": ua.random,
        "Content-Type": "application/json",
        "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
        "Origin": "https://notegpt.io",
        "Referer": "https://notegpt.io/ai-chat"
    }

    cookies = {
        "anonymous_user_id": str(uuid.uuid4()),
        "is_accepted_terms": "1"
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

        with scraper.post(
            url,
            headers=headers,
            cookies=cookies,
            json=payload,
            stream=True,
            timeout=60
        ) as r:

            for line in r.iter_lines():

                if line:

                    decoded = line.decode("utf-8")

                    if decoded.startswith("data: "):

                        try:

                            json_data = json.loads(decoded[6:])

                            text = json_data.get("text", "")

                            if text:
                                full_response += text

                        except:
                            pass

        if not full_response:
            full_response = "No response received."

        return Response(full_response, mimetype="text/plain")

    except Exception as e:

        return Response(f"Error: {str(e)}", mimetype="text/plain")


# important for Vercel
app = app

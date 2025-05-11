import requests
import json
import time
import os
import math
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

FACT_DATABASE = [
    "Twitter was founded in 2006.",
    "The character limit for a tweet is 280.",
    "Jack Dorsey is one of the founders of Twitter."
]

def validate_response(response: str, fact_database: list) -> bool:
    return any(fact.lower() in response.lower() for fact in fact_database)

def log_flagged_response(tweet: str, bot_reply: str, reason: str) -> None:
    try:
        log_entry = {
            "tweet": tweet,
            "bot_reply": bot_reply,
            "reason": reason,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        }
        with open("flagged_responses.log", "a", encoding="utf-8") as log_file:
            json.dump(log_entry, log_file)
            log_file.write("\n")
    except Exception as e:
        print(f"Logging failed: {str(e)}")

def generate_reply(tweet: str, tone_file: str = "config/tone_profile.json") -> str:
    try:
        try:
            with open(tone_file, "r", encoding="utf-8") as f:
                tone = json.load(f)
        except FileNotFoundError:
            tone = {"temperature": 0.7, "max_tokens": 150}

        messages = [
            {
                "role": "system",
                "content": (
                    "You are KGen's AI Community Bot. Provide accurate, factual information. "
                    "If unsure, respond: 'I'm not sure about that'."
                )
            },
            {"role": "user", "content": tweet}
        ]

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "KGenBot/1.0"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": messages,
            "temperature": tone.get("temperature", 0.7),
            "max_tokens": tone.get("max_tokens", 150),
            "top_p": 1.0,
            "stream": False
        }

        for attempt in range(3):
            try:
                response = requests.post(GROQ_API_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                bot_reply = data["choices"][0]["message"]["content"].strip()
                risky_topics = ["medical", "financial", "legal"]
                if any(topic in bot_reply.lower() for topic in risky_topics):
                    log_flagged_response(tweet, bot_reply, "Potentially sensitive topic")
                    return "⚠️ The bot's response may require verification due to sensitive content."
                return bot_reply
            except requests.exceptions.RequestException as e:
                delay = math.pow(2, attempt)
                print(f"[Retry {attempt + 1}/3] API call failed: {e}")
                time.sleep(delay)

        raise RuntimeError("API request failed after 3 retries")

    except Exception as e:
        log_flagged_response(tweet, str(e), "System Error")
        raise RuntimeError(f"Failed to generate reply: {str(e)}")

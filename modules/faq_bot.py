import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

class FAQBot:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.faqs = self._load_faqs()
        self.system_prompt = """
        You are a helpful FAQ assistant for KGen. Always:
        1. Answer based on provided FAQs
        2. Keep responses under 2 sentences
        3. If unsure, say "I don't have that information"
        """

    def _load_faqs(self):
        try:
            with open("data/faqs.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _call_groq_api(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 150
        }

        for attempt in range(3):
            try:
                response = requests.post(self.api_url, headers=headers, json=payload)
                response.raise_for_status()
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 10))
                    time.sleep(retry_after)
                    continue
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            except requests.exceptions.RequestException as e:
                delay = 2 ** attempt
                time.sleep(delay)
        raise RuntimeError("Failed to get response after 3 attempts")

    def get_answer(self, question):
        try:
            for faq in self.faqs:
                if faq["question"].lower() in question.lower():
                    return faq["answer"]
            return self._call_groq_api(question)
        except Exception as e:
            return f"Error: {str(e)}"

    def get_random_question(self):
        import random
        return random.choice(self.faqs)["question"] if self.faqs else "No FAQs available"

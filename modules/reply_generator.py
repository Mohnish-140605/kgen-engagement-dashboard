import openai
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_reply(tweet: str, tone_file: str = "config/tone_profile.json") -> str:
    """
    Generates a reply to a tweet based on the tone profile.

    Args:
        tweet (str): The tweet to reply to.
        tone_file (str): Path to the tone profile JSON file.

    Returns:
        str: The generated reply.
    """
    try:
        # Load tone profile
        with open(tone_file, "r", encoding="utf-8") as f:
            tone = json.load(f)

        # Construct the prompt
        prompt = f"""
You are KGen's AI Community Bot.
Style: {tone['style']}
Tweet: "{tweet}"
Reply as KGen:
"""

        # Retry logic for API calls
        for attempt in range(3):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response['choices'][0]['message']['content'].strip()
            except openai.error.RateLimitError:
                print("Rate limit hit. Retrying in 20 seconds...")
                time.sleep(20)
            except Exception as e:
                raise RuntimeError(f"An error occurred while generating the reply: {e}")

        # If all retries fail
        raise RuntimeError("Failed after 3 retries.")

    except FileNotFoundError:
        raise FileNotFoundError(f"Tone profile file not found: {tone_file}")
    except KeyError as e:
        raise KeyError(f"Missing key in tone profile: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the reply: {e}")

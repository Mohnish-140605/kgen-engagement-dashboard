import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

def fetch_mentions(count: int = 10, simulate_errors: bool = False) -> List[Dict]:
    if simulate_errors:
        raise Exception("API Error 429: Rate limit exceeded - Try again in 15 minutes")
    
    base_tweets = [
        {
            "text": "Loving the AI vibes! How do I get started?",
            "sentiment": "positive",
            "lang": "en",
            "type": "question"
        },
        {
            "text": "Your last post was 🔥! Got more insights?",
            "sentiment": "positive", 
            "lang": "en",
            "type": "engagement"
        },
        {
            "text": "I'm facing issues with setup. Can you help? 😕",
            "sentiment": "negative",
            "lang": "en",
            "type": "support"
        },
        {
            "text": "¿KGen es de código abierto o comercial?",
            "sentiment": "neutral",
            "lang": "es",
            "type": "question"
        },
        {
            "text": "This is useless! Waste of time. 💩",
            "sentiment": "negative",
            "lang": "en",
            "type": "complaint"
        },
        {
            "text": "Can AI replace human creativity? What's your take? 🤖",
            "sentiment": "neutral",
            "lang": "en",
            "type": "discussion"
        },
        {
            "text": "如何将KGen集成到现有工具中？",
            "sentiment": "neutral",
            "lang": "zh",
            "type": "question"
        }
    ]

    mentions = []
    for i in range(count):
        tweet = random.choice(base_tweets).copy()
        mention = {
            "id": str(random.randint(1000000000000000000, 9999999999999999999)),
            "text": f"@kgenio {tweet['text']}",
            "user": {
                "screen_name": random.choice(["tech_enthusiast42", "ai_researcher", "dev_007", 
                                            "startup_founder", "coder_girl", "ml_master"]),
                "followers_count": random.randint(0, 100000),
                "verified": random.choice([True, False])
            },
            "created_at": (datetime.now() - timedelta(minutes=random.randint(0, 10080))).isoformat(),
            "lang": tweet["lang"],
            "metrics": {
                "likes": random.randint(0, 500),
                "retweets": random.randint(0, 100),
                "replies": random.randint(0, 50)
            },
            "sentiment": tweet["sentiment"],
            "type": tweet["type"]
        }
        
        if random.random() > 0.7:
            mention["text"] += " https://example.com"
            
        mentions.append(mention)

    for mention in mentions:
        if random.random() > 0.9:
            mention["user"]["verified"] = None

    random.shuffle(mentions)
    
    return mentions[:count]

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

def fetch_mentions(count: int = 10, simulate_errors: bool = False) -> List[Dict]:
    """
    Generates realistic simulated Twitter mentions with comprehensive metadata
    
    Args:
        count: Number of mentions to return (default: 10)
        simulate_errors: Whether to simulate API errors (default: False)
        
    Returns:
        List of mention dictionaries with full metadata
        
    Example:
        >>> mentions = fetch_mentions(5)
        >>> len(mentions)
        5
    """
    if simulate_errors:
        # Simulate rate limit error
        raise Exception("API Error 429: Rate limit exceeded - Try again in 15 minutes")
    
    # Base dataset with enhanced metadata
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

    # Generate dynamic mentions
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
        
        # Add optional URL
        if random.random() > 0.7:
            mention["text"] += " https://example.com"
            
        mentions.append(mention)

    # Add random null values to simulate real API data
    for mention in mentions:
        if random.random() > 0.9:
            mention["user"]["verified"] = None

    # Shuffle to simulate real API order
    random.shuffle(mentions)
    
    return mentions[:count]

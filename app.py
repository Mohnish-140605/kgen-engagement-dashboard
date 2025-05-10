import streamlit as st
from modules import twitter_api, reply_generator, sentiment
import pandas as pd
import json, os

st.set_page_config(page_title="KGen Engagement Bot", layout="wide")
st.title("🤖 KGen AI Community Bot")

# Load tweets
tweets = twitter_api.fetch_mentions()
st.sidebar.header("Tweets")
tweet_texts = [f"{t['id']} - {t['text']}" for t in tweets]
selected = st.sidebar.selectbox("Select a tweet", tweet_texts)
tweet = next(t for t in tweets if selected.startswith(t['id']))

st.subheader("📨 Tweet Content")
st.write(tweet['text'])

# Generate reply
reply = reply_generator.generate_reply(tweet['text'])
st.subheader("💬 AI-Generated Reply")
st.code(reply, language='markdown')

# Sentiment
sent = sentiment.analyze_sentiment(tweet['text'])
st.subheader("🧠 Sentiment")
st.success(sent if sent != "Negative" else f"⚠️ {sent}")

# Feedback
if st.button("👍 Approve"):
    log = pd.DataFrame([[tweet['id'], tweet['text'], reply, "Approved"]])
    log.to_csv("data/feedback_log.csv", mode='a', header=False, index=False)
    st.success("Approved and logged!")

if st.button("👎 Needs Edit"):
    st.text_area("Suggest your edit", key="edit")

import streamlit as st
from modules import reply_generator, sentiment, twitter_predefined_texts
import pandas as pd
import random
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="KGen Engagement Bot", layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    .stApp {
        background-image: url('https://www.transparenttextures.com/patterns/robots.png');
        background-size: cover;
    }
    .header {
        font-family: 'Press Start 2P', cursive;
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
        white-space: nowrap;
        overflow: hidden;
        border-right: 3px solid #4CAF50;
        animation: typing 4s steps(40, end), blink 0.75s step-end infinite, reset 8s infinite;
    }
    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }
    @keyframes blink {
        50% { border-color: transparent; }
    }
    @keyframes reset {
        0%, 90% { opacity: 1; }
        91%, 100% { opacity: 0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='header'>🤖 Welcome to the KGen AI Dashboard! 🚀</div>", unsafe_allow_html=True)

st.sidebar.header("📋 Navigation")
st.sidebar.markdown("Use the options below to explore the dashboard:")
st.sidebar.markdown("1. Select a tweet to analyze.")
st.sidebar.markdown("2. Play trivia or guessing games.")
st.sidebar.markdown("3. Interact with the KGen bot.")
st.sidebar.markdown("4. Test your typing speed!")

tweets = twitter_predefined_texts.fetch_mentions()
st.sidebar.subheader("Tweets")
tweet_texts = [f"{t['id']} - {t['text']}" for t in tweets]
selected = st.sidebar.selectbox("Select a tweet", tweet_texts)
tweet = next(t for t in tweets if selected.startswith(t['id']))

st.markdown("<div class='subheader'>📨 Tweet Content</div>", unsafe_allow_html=True)
st.write(tweet['text'])

st.markdown("<div class='subheader'>💬 AI-Generated Reply</div>", unsafe_allow_html=True)
with st.spinner("🤖 Generating reply..."):
    reply = reply_generator.generate_reply(tweet['text'])
st.code(reply, language='markdown')

st.markdown("<div class='subheader'>🧠 Sentiment Analysis</div>", unsafe_allow_html=True)
sent = sentiment.analyze_sentiment(tweet['text'])
if sent == "Positive":
    st.success(f"Sentiment: {sent}")
elif sent == "Neutral":
    st.info(f"Sentiment: {sent}")
else:
    st.error(f"Sentiment: {sent}")

st.markdown("<div class='subheader'>⌨️ Typing Speed Test</div>", unsafe_allow_html=True)

if "typing_test_started" not in st.session_state:
    st.session_state.typing_test_started = False
    st.session_state.start_time = None
    st.session_state.test_text = None
    st.session_state.user_input = ""

if not st.session_state.typing_test_started:
    if st.button("Start Typing Test"):
        st.session_state.typing_test_started = True
        st.session_state.start_time = time.time()
        st.session_state.test_text = random.choice([
            "The quick brown fox jumps over the lazy dog.",
            "Artificial intelligence is transforming the world.",
            "Streamlit makes building web apps easy and fun.",
            "KGen is revolutionizing the way we interact with AI."
        ])
else:
    st.write("Type the following text as quickly as you can:")
    st.markdown(f"**{st.session_state.test_text}**")
    st.session_state.user_input = st.text_area("Start typing here:", height=100)

    if st.button("Submit"):
        end_time = time.time()
        elapsed_time = end_time - st.session_state.start_time
        words_typed = len(st.session_state.user_input.split())
        correct_words = sum(
            1 for a, b in zip(st.session_state.user_input.split(), st.session_state.test_text.split()) if a == b
        )
        accuracy = (correct_words / len(st.session_state.test_text.split())) * 100

        st.success(f"🎉 Typing Test Completed!")
        st.write(f"⏱️ Time Taken: {elapsed_time:.2f} seconds")
        st.write(f"💬 Words Typed: {words_typed}")
        st.write(f"✅ Accuracy: {accuracy:.2f}%")

        st.session_state.typing_test_started = False

st.markdown("<div class='subheader'>☁️ Word Cloud of Tweets</div>", unsafe_allow_html=True)
all_tweets = " ".join([t['text'] for t in tweets])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_tweets)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

st.markdown("<div class='subheader'>💬 Chat with KGen Bot</div>", unsafe_allow_html=True)
st.image(
    "https://media.giphy.com/media/PI3QGKFN6XZUCMMqJm/giphy.gif",
    width=150,
    caption="KGen Bot is listening..."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Say something to the bot:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    bot_reply = reply_generator.generate_reply(user_input)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

st.markdown("<div class='subheader'>📊 Feedback Progress</div>", unsafe_allow_html=True)
reviewed = len(pd.read_csv("data/feedback_log.csv"))
total = len(tweets)
progress = reviewed / total
st.progress(progress)
st.write(f"Reviewed {reviewed} out of {total} tweets.")

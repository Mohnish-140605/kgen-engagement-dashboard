
---

# 🚀 KGen Engagement Dashboard

A Streamlit-powered dashboard for KGen that uses AI to analyze Twitter mentions, generate smart replies, visualize trends, and engage users with games-all in one interactive app. Powered by Groq API and TextBlob.

---

## ✨ Features

- 🤖 **AI Chatbot**: Chat with KGen Bot using Groq’s Llama3 model  
- 🧠 **Sentiment Analysis**: Detects tweet sentiment using TextBlob  
- 📊 **Word Cloud**: Visualizes trending words from tweets  
- 🎮 **Trivia & Games**: Play Twitter trivia and sentiment guessing  
- 📈 **Feedback Tracker**: See your engagement progress  
- 🔒 **Secure**: API keys are never committed

---

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/kgen-engagement-dashboard.git
   cd kgen-engagement-dashboard
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Setting Up Your `.env` File

1. **Create a `.env` file** in the project root (same folder as `app.py`):

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   **Never share or commit your `.env` file!**

---

## 📝 How to Get Your Groq API Key

1. Go to [Groq Cloud Console](https://console.groq.com/keys)
2. Log in or sign up for an account
3. Click **Create API Key**
4. Copy your new API key and paste it into your `.env` file as shown above

---

## 🚦 Running the App

```bash
streamlit run app.py
```

- The dashboard will open in your browser at `http://localhost:8501`
- Select tweets, chat with the bot, play games, and visualize engagement!

---

## 🧩 Project Structure

```
kgen-engagement-dashboard/
├── app.py
├── modules/
│   ├── reply_generator.py
│   ├── sentiment.py
│   └── twitter_predefined_texts.py
├── config/
│   └── tone_profile.json
├── data/
│   └── feedback_log.csv
├── requirements.txt
└── .env           # <-- You create this!
```

---

## 🛡️ Security Best Practices

- `.env` and `venv/` are in `.gitignore` and **should never be committed**
- If you accidentally commit secrets, [remove them from git history](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

---

## 🤝 Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT

---

**Enjoy building with KGen Engagement Dashboard! 🚀**

---


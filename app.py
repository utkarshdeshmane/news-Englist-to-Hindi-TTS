import streamlit as st
import os
from api import fetch_news
from utils import summarize_text, analyze_sentiment, translate_to_hindi, text_to_speech_google
from gtts import gTTS

# UI Config
st.set_page_config(page_title="🗞️ News Summarization & Hindi TTS", layout="wide", page_icon="🗞️")

# Inject Custom Dark Theme
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #121212;
            color: #f5f5f5;
        }
        .title {
            font-size: 40px;
            font-weight: 700;
            color: #00adb5;
            text-align: center;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            color: #aaa;
            font-size: 18px;
            margin-bottom: 40px;
        }
        .stTextInput > div > div > input {
            background-color: #1e1e1e;
            color: #f5f5f5;
        }
        .stTextInput > div > label {
            color: #bbb;
        }
        .stButton button {
            background-color: #00adb5;
            color: white;
        }
        a {
            color: #00adb5 !important;
        }
        .stAudio {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📰 News Summarization & Hindi TTS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Summarize latest news, analyze sentiment, and listen in Hindi!</div>', unsafe_allow_html=True)

# Sidebar Input
st.sidebar.header("🔍 Search News")
company = st.sidebar.text_input("Enter Company Name", "Tesla")

if st.sidebar.button("Fetch News"):
    with st.spinner("⏳ Fetching latest news..."):
        articles = fetch_news(company)

    if not articles:
        st.error("❌ No news found! Try another keyword.")
    else:
        st.success(f"✅ Found {len(articles)} articles on **{company}**.")
        summaries = []

        for i, article in enumerate(articles, 1):
            with st.container():
                st.markdown("---")
                st.subheader(f"📰 {i}. {article['title']}")
                st.markdown(f"🔗 [Read Full Article]({article['url']})")

                if 'summary' not in article or not article['summary']:
                    st.warning("⚠️ No summary available. Skipping this article.")
                    continue

                summary = summarize_text(article['summary'])
                sentiment, score = analyze_sentiment(summary)
                hindi_summary = translate_to_hindi(summary)

                st.markdown(f"📝 **Summary:** {summary}")
                st.markdown(f"📊 **Sentiment:** {sentiment} (Score: {score:.2f})")
                st.markdown(f"🈳 **Hindi Summary:** {hindi_summary}")

                summaries.append(f"{i}. {hindi_summary}")

        if summaries:
            final_text = "\n".join(summaries)
            audio_file = text_to_speech_google(final_text)

            st.markdown("---")
            st.subheader("🔉 Hindi Audio Summary")
            st.audio(audio_file, format="audio/mp3", start_time=0)

            with open(audio_file, "rb") as f:
                st.download_button("⬇ Download Hindi Audio", f, file_name="news_summary.mp3")

            os.remove(audio_file)
        else:
            st.error("❌ No valid summaries to convert to speech.")

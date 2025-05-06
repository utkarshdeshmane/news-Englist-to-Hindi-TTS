import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from deep_translator import GoogleTranslator  
from gtts import gTTS


# Download NLTK dependencies
nltk.download("vader_lexicon")

# Load models globally for efficiency
sia = SentimentIntensityAnalyzer()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Better model

def summarize_text(text):
    """Summarizes text using a Transformer model."""
    if len(text.split()) < 20:  # Avoid summarizing very short text
        return text
    return summarizer(text, max_length=50, min_length=10, do_sample=False)[0]["summary_text"]

def analyze_sentiment(text):
    """Analyzes sentiment using Vader Sentiment Analyzer."""
    score = sia.polarity_scores(text)["compound"]
    return (
        "Positive" if score >= 0.05 else
        "Negative" if score <= -0.05 else
        "Neutral", score
    )

def translate_to_hindi(text):
    """Translates English text to Hindi using Deep Translator."""
    return GoogleTranslator(source="auto", target="hi").translate(text)  # ✅ Updated Translation Function

def text_to_speech_google(text, filename="news_summary.mp3"):
    """Converts text to Hindi speech using Google TTS."""
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(filename)
    return filename

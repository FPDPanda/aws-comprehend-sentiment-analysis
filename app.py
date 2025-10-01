import streamlit as st
import pandas as pd
from datetime import datetime
from services.comprehend_service import create_comprehend_service

st.set_page_config(
    page_title="AWS Comprehend Sentiment Analysis",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AWS Comprehend Sentiment Analysis")
st.markdown("Analyze text sentiment using AWS Comprehend's powerful NLP capabilities.")

tab1, tab2 = st.tabs(["Single Text Analysis", "About"])
comprehend_service = create_comprehend_service()

with tab1:
    st.header("Single Text Analysis")
    
    text_input = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="Type your text here...",
        help="Enter any text you want to analyze for sentiment"
    )
    
    if st.button("Analyze Sentiment", type="primary"):
        if text_input.strip():
            with st.spinner("Analyzing sentiment..."):
                try:
                    sentiment_api_response = comprehend_service.analyze_sentiment(text_input.strip())
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        sentiment = sentiment_api_response['sentiment']
                        color_map = {
                            'POSITIVE': '🟢',
                            'NEGATIVE': '🔴', 
                            'NEUTRAL': '🟡',
                            'MIXED': '🟠'
                        }
                        st.metric(
                            label="Overall Sentiment",
                            value=f"{color_map.get(sentiment, '⚪')} {sentiment.title()}"
                        )
                    
                    with col2:
                        scores = sentiment_api_response['sentiment_score']
                        st.write("**Confidence Scores:**")
                        for sentiment_type, score in scores.items():
                            st.progress(score, text=f"{sentiment_type}: {score:.1%}")
                            
                except Exception as e:
                    st.error(f"Error analyzing text: {str(e)}")
        else:
            st.warning("Please enter some text to analyze.")

with tab2:
    st.header("About")
    st.markdown("""
    This application uses **AWS Comprehend** to perform sentiment analysis on text data.
    
    **Features:**
    - Single text sentiment analysis
    - Real-time sentiment scoring
    - Visual results display
    
    **Supported Sentiments:**
    - 🟢 Positive
    - 🔴 Negative  
    - 🟡 Neutral
    - 🟠 Mixed
    """)

with st.sidebar:
    st.subheader("Analysis Settings")
    language_code = st.selectbox(
        "Language",
        ["en", "es", "fr", "de", "it", "pt", "ja"],
        index=0
    )

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    pass
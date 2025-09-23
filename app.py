import streamlit as st
import pandas as pd
from datetime import datetime
from services.comprehend_service import create_comprehend_service

# Set page configuration - this should be the first Streamlit command
st.set_page_config(
    page_title="AWS Comprehend Sentiment Analysis",
    page_icon="🔍",
    layout="wide"
)

# Main title and description
st.title("🔍 AWS Comprehend Sentiment Analysis")
st.markdown("Analyze text sentiment using AWS Comprehend's powerful NLP capabilities.")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Single Text Analysis", "Batch Analysis", "About"])
comprehend_service = create_comprehend_service()

with tab1:
    st.header("Single Text Analysis")
    
    # Text input area
    text_input = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="Type your text here...",
        help="Enter any text you want to analyze for sentiment"
    )
    
    # Analyze button
    if st.button("Analyze Sentiment", type="primary"):
        if text_input.strip():
            with st.spinner("Analyzing sentiment..."):
                try:
                    comprehend_service.analyze_sentiment(text_input.strip())
                    # This is where you'll call AWS Comprehend
                    # comprehend = get_comprehend_client()
                    # response = comprehend.detect_sentiment(Text=text_input, LanguageCode='en')
                    
                    # For now, let's use mock data
                    mock_sentiment = {
                        'Sentiment': 'POSITIVE',
                        'SentimentScore': {
                            'Positive': 0.95,
                            'Negative': 0.02,
                            'Neutral': 0.02,
                        }
                    }
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        sentiment = mock_sentiment['Sentiment']
                        color_map = {
                            'POSITIVE': '🟢',
                            'NEGATIVE': '🔴', 
                            'NEUTRAL': '🟡',
                        }
                        st.metric(
                            label="Overall Sentiment",
                            value=f"{color_map.get(sentiment, '⚪')} {sentiment.title()}"
                        )
                    
                    with col2:
                        scores = mock_sentiment['SentimentScore']
                        st.write("**Confidence Scores:**")
                        for sentiment_type, score in scores.items():
                            st.progress(score, text=f"{sentiment_type}: {score:.1%}")
                            
                except Exception as e:
                    st.error(f"Error analyzing text: {str(e)}")
        else:
            st.warning("Please enter some text to analyze.")

with tab2:
    st.header("Batch Analysis")
    st.info("Upload a CSV file with a 'text' column for batch analysis.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {len(df)} records")
            st.dataframe(df.head())
            
            if st.button("Analyze Batch", type="primary"):
                # Batch analysis logic would go here
                st.info("Batch analysis feature coming soon!")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

with tab3:
    st.header("About")
    st.markdown("""
    This application uses **AWS Comprehend** to perform sentiment analysis on text data.
    
    **Features:**
    - Single text sentiment analysis
    - Batch analysis from CSV files
    - Real-time sentiment scoring
    - Visual results display
    
    **Supported Sentiments:**
    - 🟢 Positive
    - 🔴 Negative  
    - 🟡 Neutral
    """)

# Sidebar for configuration
with st.sidebar:
    st.subheader("Analysis Settings")
    language_code = st.selectbox(
        "Language",
        ["en", "es", "fr", "de", "it", "pt", "ja"],
        index=0
    )

# Footer
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # This is automatically handled by Streamlit
    pass
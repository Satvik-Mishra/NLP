import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

# Set page title and description for Sentiment Analysis
st.title("SENTIMENT ANALYSIS")
st.write("Enter text or upload a document to discover the sentiment!")

# User input for text or document upload (Sentiment Analysis)
user_input_sentiment = st.text_area("Enter text here:")
st.subheader("OR")
uploaded_file_sentiment = st.file_uploader("Upload a document", type=["txt"])




# Set page title and description for Keyword Analysis
st.title("KEYWORD ANALYSER")
st.write("Enter text or upload a document to analyze keywords.")

# User input for text or document upload (Keyword Analysis)
user_input_keywords = st.text_area("Enter your text")
st.subheader("OR")
uploaded_file_keywords = st.file_uploader("Upload a document", type=["txt"], key="keywords")

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity
    return polarity, subjectivity

# Function to process text and extract keywords
def process_text(text):
    if uploaded_file_keywords:
        text = text.decode('utf-8')
    
    words = word_tokenize(text.lower())  # Tokenize and decode the bytes to string
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words and word not in string.punctuation]
    word_freq = nltk.FreqDist(filtered_words)
    return word_freq

# Analyze sentiment based on user input (Sentiment Analysis)

    
if user_input_sentiment:
    polarity, subjectivity = analyze_sentiment(user_input_sentiment)
    sentiment = "Positive" if polarity > 0 else ("Negative" if polarity < 0 else "Neutral")
    st.write(f"Sentiment: {sentiment}")
    st.write(f"Polarity: {polarity}")
    st.write(f"Subjectivity: {subjectivity}")
    data = pd.DataFrame({'Sentiment': [sentiment], 'Polarity': [polarity], 'Subjectivity': [subjectivity]})
    st.bar_chart(data.set_index('Sentiment'))
elif uploaded_file_sentiment is not None:
    file_content = uploaded_file_sentiment.read()
    show_text_sentiment = st.button("Show Document Text")
    
    
    
    # If the button is clicked, display the document text
    if show_text_sentiment:
        st.write(file_content)
        hide_button_sentiment = st.button("Hide Document Text")
        
        # If the hide button is clicked, clear the document text
        if hide_button_sentiment:
            st.text("")  # Empty space to clear the displayed text
    
    polarity, subjectivity = analyze_sentiment(file_content.decode("utf-8"))
    sentiment = "Positive" if polarity > 0 else ("Negative" if polarity < 0 else "Neutral")
    st.write(f"Sentiment: {sentiment}")
    st.write(f"Polarity: {polarity}")
    st.write(f"Subjectivity: {subjectivity}")
    data = pd.DataFrame({'Sentiment': [sentiment], 'Polarity': [polarity], 'Subjectivity': [subjectivity]})
    st.bar_chart(data.set_index('Sentiment'))
  

# Process text and extract keywords (Keyword Analysis)
if user_input_keywords:
    word_freq = process_text(user_input_keywords)
    display_keywords = True
elif uploaded_file_keywords is not None:
    file_content_keywords = uploaded_file_keywords.read()
    word_freq = process_text(file_content_keywords)
    display_keywords = True
else:
    display_keywords = False

    

# Display keywords and plot the top words
if display_keywords:
    st.title("RESULTS")
    st.write("Common Keywords in Text:")
    top_words = dict(word_freq.most_common(15))
    lessw=dict(word_freq.most_common(5))
    top5 = st.button("Show Only Top 5", key=6)
    if top5:
        st.table(pd.DataFrame(list(lessw.items()), columns=['Word', 'Frequency']))
    

    else:    
        data = {'Word': [], 'Frequency': []}
    
        st.table(pd.DataFrame(list(top_words.items()), columns=['Word', 'Frequency']))
        
        # Plotting the top words
    fig, ax = plt.subplots()
        
    sns.barplot(x=list(top_words.values()), y=list(top_words.keys()))
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.title('Word Frequencies')
    st.pyplot(fig)

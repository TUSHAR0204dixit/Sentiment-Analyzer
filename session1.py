import streamlit as st
import pandas as pd
from textblob import TextBlob
import tweepy
import plotly.express as px
import os

# --- Twitter API Setup ---
BEARER_TOKEN ='AAAAAAAAAAAAAAAAAAAAAI%2BR0gEAAAAAWYwDrrxTrCLByJnlEqn5mHzotAA%3DTOBz1Yogg0bXe74FCUoreBwXJCxZ3uTHW7ThmGbheSWmCSDa0A'
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# --- Streamlit UI ---
st.title("🔍 AI-Powered Sentiment Analyzer for Brand Monitoring")
brand = st.text_input("Enter a brand or keyword to analyze tweets:", value="Nike")

if st.button("Analyze Tweets"):
    with st.spinner("Fetching tweets..."):
        # Query to fetch tweets related to the entered brand
        query = f'{brand} -is:retweet lang:en'

        try:
            # Fetch tweets
            tweets = client.search_recent_tweets(query=query, max_results=50, tweet_fields=['created_at', 'text'])

            if tweets.data:
                data = []
                for tweet in tweets.data:
                    text = tweet.text
                    score = TextBlob(text).sentiment.polarity

                    if score > 0.1:
                        sentiment = 'Positive'
                    elif score < -0.1:
                        sentiment = 'Negative'
                    else:
                        sentiment = 'Neutral'

                    # Append tweet data
                    data.append({'Time': tweet.created_at, 'Tweet': text, 'Sentiment': sentiment})

                # Create DataFrame from tweet data
                df = pd.DataFrame(data)

                # --- Display Table ---
                st.subheader("📋 Tweet Sentiment Table")
                st.dataframe(df)

                # --- Pie Chart ---
                st.subheader("📊 Sentiment Distribution")
                fig = px.pie(df, names='Sentiment', title='Sentiment Breakdown')
                st.plotly_chart(fig)

                # --- Line Chart: Sentiment Over Time ---
                st.subheader("📈 Sentiment Over Time")
                fig_time = px.line(df, x='Time', color='Sentiment', title='Timeline of Sentiments')
                st.plotly_chart(fig_time)

            else:
                st.warning("No tweets found for this brand. Please try another brand or keyword.")
        except tweepy.TweepyException as e:
            st.error(f"An error occurred while fetching tweets: {str(e)}")

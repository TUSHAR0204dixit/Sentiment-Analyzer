import streamlit as st
import pandas as pd
from textblob import TextBlob
import tweepy
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt


BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAETU4AEAAAAACzcMUYKd0MXGEVPeln5tTPOBp5Q%3Dr6ioTfyaaEzZ2i05Z5Wyta5MOZAr1UD2sMBT4Q0nV5dBTUU2Bb"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# --- Streamlit UI ---
st.title("🔍 AI-Powered Sentiment Analyzer for Brand Monitoring")
brand = st.text_input("Enter a brand or keyword to analyze tweets:", value="Nike")

if st.button("Analyze Tweets"):
    with st.spinner("Fetching tweets..."):
        query = f'{brand} -is:retweet lang:en'

        try:
            tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at', 'text'])

            if not tweets or not tweets.data:
                st.warning("No tweets found for this brand. Please try another keyword.")
            else:
                data = []
                for tweet in tweets.data:
                    text = tweet.text
                    score = TextBlob(text).sentiment.polarity

                    if score >= 0.3:
                        sentiment = 'Positive'
                    elif score <= -0.3:
                        sentiment = 'Negative'
                    else:
                        sentiment = 'Neutral'

                    data.append({'Time': tweet.created_at, 'Tweet': text, 'Sentiment': sentiment})

                df = pd.DataFrame(data)
                df['Time'] = pd.to_datetime(df['Time'])

                # --- Display Table ---
                st.subheader("📋 Tweet Sentiment Table")
                st.dataframe(df)

                # --- Pie Chart ---
                st.subheader("📊 Sentiment Distribution")
                fig = px.pie(df, names='Sentiment', title='Sentiment Breakdown')
                st.plotly_chart(fig)

                # --- Line Chart ---
                st.subheader("📈 Sentiment Over Time")
                timeline = df.groupby([pd.Grouper(key='Time', freq='5min'), 'Sentiment']).size().reset_index(name='Count')
                fig_time = px.line(timeline, x='Time', y='Count', color='Sentiment', title='Timeline of Sentiments')
                st.plotly_chart(fig_time)

                # --- Word Cloud ---
                st.subheader("☁️ Common Words in Tweets")
                text_combined = " ".join(df['Tweet'])
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_combined)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)

                # --- Personalized Ad Recommendations ---
                st.subheader("🧠 Personalized Ad Recommendations")

                pos_pct = (df['Sentiment'] == 'Positive').mean() * 100
                neg_pct = (df['Sentiment'] == 'Negative').mean() * 100
                neu_pct = (df['Sentiment'] == 'Neutral').mean() * 100

                if pos_pct > 50:
                    st.success("✅ High Positive Sentiment: Promote user testimonials and influencer campaigns.")
                elif neg_pct > 30:
                    st.error("⚠️ High Negative Sentiment: Focus on customer support and damage control ads.")
                else:
                    st.info("ℹ️ Neutral Sentiment: Run awareness campaigns or highlight USPs.")

                # --- Predictive Campaign Analytics ---
                st.subheader("📈 Predictive Campaign Performance Analytics")

                tweet_volume = len(df)
                if pos_pct > 50 and tweet_volume > 30:
                    prediction = "🔥 High chance of campaign success!"
                elif neg_pct > 40:
                    prediction = "❌ Campaign risk: High negative sentiment detected."
                elif tweet_volume < 10:
                    prediction = "🤏 Low data: Campaign impact might be limited."
                else:
                    prediction = "🟡 Moderate chance of campaign success."

                st.markdown(f"**Prediction:** {prediction}")

        except tweepy.TweepyException as e:
            st.error(f"An error occurred while fetching tweets: {str(e)}")

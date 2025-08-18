import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_KEY_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)

def scrape_user_tweets(username: str, num_tweet: int = 5, mock: bool = False):
    """
    Scrape a Twitter user's original tweets (not retweets or replies).
    Returns a list of dicts with: {"text": ..., "url": ...}
    """
    tweet_list = []

    try:
        if mock:
            # Use a gist for demo/testing
            EDEN_TWITTER_GIST = (
                "https://gist.githubusercontent.com/emarco177/"
                "827323bb599553d0f0e662da07b9ff68/raw/"
                "57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json"
            )
            tweets = requests.get(EDEN_TWITTER_GIST).json()
        else:
            # Get user ID
            user_resp = twitter_client.get_user(username=username)
            if not user_resp.data:
                print(f"User not found: {username}")
                return []

            user_id = user_resp.data.id

            # Get tweets
            tweets = twitter_client.get_users_tweets(
                id=user_id,
                max_results=num_tweet,
                exclude=["retweets", "replies"]
            ).data or []  # prevent None

        # Normalize to list of dicts
        for tweet in tweets:
            tweet_list.append({
                "text": tweet["text"],
                "url": f"https://x.com/{username}/status/{tweet['id']}",
            })

    except Exception as e:
        print(f" Error fetching tweets for {username}: {e}")

    return tweet_list


if __name__ == "__main__":
    tweets = scrape_user_tweets(username="EdenEmarco177", num_tweet=5)
    for t in tweets:
        print(f"- {t['url']}\n  {t['text']}\n")

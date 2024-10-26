# import requests

# def fetch_trending_topics():
#     url = f'https://api.twitter.com/2/tweets/search/recent'
#     headers = {"Authorization": f"Bearer YOUR_API_KEY"}
#     response = requests.get(url, headers=headers)
#     return response.json().get('data', [])

from pytrends.request import TrendReq

def fetch_trending_topics():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending = pytrends.trending_searches(pn='india')  # Fetches trending topics for India
    return trending[0].tolist()# List of trending topics

def fetch_interest_over_time(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='', gprop='')
    data = pytrends.interest_over_time()
    return data

def fetch_related_queries(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='', gprop='')
    related_queries = pytrends.related_queries()
    return related_queries[keyword]['top']

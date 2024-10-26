# from django.shortcuts import render
# from .models import MemeTemplate
# from .utils import fetch_trending_topics  # Assuming fetch_trending_topics in utils.py

# def meme_list(request):
#     topics = fetch_trending_topics()
#     templates = MemeTemplate.objects.all()
#     return render(request, 'memes/meme_list.html', {'topics': topics, 'templates': templates})

# # In memes/views.py
# from django.http import JsonResponse

# def trending_topics_api(request):
#     topics = fetch_trending_topics()
#     return JsonResponse({"topics": topics})

# from pytrends.request import TrendReq

# def fetch_trending_topics():
#     pytrends = TrendReq(hl='en-US', tz=360)  # 'hl' sets language, 'tz' sets timezone
#     trending = pytrends.trending_searches(pn='united_states')  # You can change to any supported region
#     return trending[0].tolist()  # Returns a list of trending topics
    
# trends = fetch_trending_topics()
# print("Current Trending Topics:", trends)

# def fetch_interest_over_time(keyword):
#     pytrends = TrendReq(hl='en-US', tz=360)
#     pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='', gprop='')
#     data = pytrends.interest_over_time()
#     return data

# def fetch_related_queries(keyword):
#     pytrends = TrendReq(hl='en-US', tz=360)
#     pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='', gprop='')
#     related_queries = pytrends.related_queries()
#     return related_queries[keyword]['top']


from django.http import JsonResponse
from .utils import fetch_trending_topics
import os
from django.conf import settings
from django.shortcuts import render

def trending_topics_api(request):
    trending_topics = fetch_trending_topics()
    return JsonResponse({'trending_topics': trending_topics})

# def meme_list(request):
#     meme_dir = os.path.join(settings.MEDIA_ROOT, 'memes')
#     meme_files = os.listdir(meme_dir)
#     meme_files = [f for f in meme_files if f.endswith(('.png', '.jpg', '.jpeg'))]  # Filter for image files
#     return render(request, 'meme_list.html', {'meme_files': meme_files})



def meme_list(request):
    memes = os.listdir(os.path.join(settings.MEDIA_ROOT, 'memes'))  # List files in media/memes
    return render(request, 'meme_list.html', {'memes': memes})
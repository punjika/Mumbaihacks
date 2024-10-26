from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('trending/', views.trending_topics_api, name='trending_topics_api'),
    path('memes/', views.meme_list, name='meme_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('explore/', views.ExploreView.as_view(), name='explore'),
    path('insights/', views.insights_view, name='insights'),
    path('tweet/<int:pk>/', views.TweetDetailView.as_view(), name='tweet-detail'),
    path('tweet/new/', views.TweetCreateView.as_view(), name='tweet-create'),
    path('tweet/new/poll/', views.create_poll, name='create-poll'),
    path('tweet/new/event/', views.create_event, name='create-event'),
    path('tweet/<int:pk>/update/', views.TweetUpdateView.as_view(), name='tweet-update'),
    path('tweet/<int:pk>/delete/', views.TweetDeleteView.as_view(), name='tweet-delete'),
    path('tweet/<int:pk>/like/', views.tweet_like, name='tweet-like'),
    path('tweet/<int:pk>/retweet/', views.retweet, name='retweet'),
    path('tweet/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('poll/<int:pk>/vote/', views.vote_poll, name='vote-poll'),
    path('search/', views.SearchView.as_view(), name='search'),
]

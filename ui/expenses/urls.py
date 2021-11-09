from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('check/', views.check, name='data_check'),
    # path('user/<str:author>', views.author_articles, name='user_articles'),
    # path('topic/<str:topic>', views.topic_articles, name='topic_articles'),
    # path('article/<str:slug>', views.single_article, name='single_article')
]

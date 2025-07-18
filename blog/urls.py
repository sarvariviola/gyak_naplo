from django.urls import path, include
from . import views
from .views import chatbot_api

urlpatterns = [ 
     path('', views.index, name='index'),
     path('register/', views.register_view, name='register'),
     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
     path('blogs', views.blog_list, name='blog_list'),
     path('blog_create/', views.blog_create, name='blog_create'),
     path('profile/', views.profile, name='profile'),
     path('gallery/', views.gallery_view, name='gallery'),
     path('chatbot/', chatbot_api, name='chatbot_api'),
]

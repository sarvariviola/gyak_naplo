"""
URL configuration for dailycalendar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse
from django.http import HttpResponseRedirect

from blog import views

def root_redirect(request):
    return HttpResponseRedirect(reverse('login'))

urlpatterns = [
    path('', root_redirect),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('index/', views.index, name='index'),
    path('register/', views.register_view, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('blog/pdf/', views.blog_list_pdf, name='blog_list_pdf'),
    path('chat/', views.chatbot_api, name="chatbot")
    
] + static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

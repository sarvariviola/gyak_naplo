from django.shortcuts import render, redirect

import blog
from .models import Blog, User, Picture
from .forms import BlogForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.conf import settings
from .forms import BlogDateFilterForm
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse

import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import environ
env = environ.Env()

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "register.html", { "form": form })

def login_view(request): 
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())
            return redirect("index")
    else: 
        form = AuthenticationForm()
    return render(request, "login.html", { "form": form })

def blog_list(request):
    form = BlogDateFilterForm(request.GET or None)
    blogs = Blog.objects.filter(user=request.user).order_by('-timestamp')

    selected_category = request.GET.get('category')
    if selected_category:
            blogs = blogs.filter(category=selected_category)

    categories = Blog.objects.filter(user=request.user).values_list('category', flat=True).distinct()

    if form.is_valid() and form.cleaned_data['date']:
        blogs = blogs.filter(timestamp__date=form.cleaned_data['date'])

    return render(request, 'blog_list.html', {
        'blogs': blogs,
        'categories': categories,
        'form': form,
        'selected_category' : selected_category,
        'MEDIA_URL': settings.MEDIA_URL,})

def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog_create.html', {'form': form})

def logout_view(request) :
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    return render(request, 'profile.html')

@login_required(login_url='/login/')
def gallery_view(request):
    blogs = Blog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'gallery.html', {
        'blogs': blogs,
        'MEDIA_URL': settings.MEDIA_URL,})

def blog_list_pdf(request):
    blogs = Blog.objects.filter(user=request.user).order_by('-timestamp')

    template = get_template('blog_list.html')
    html_string = template.render({'blogs': blogs, 'user': request.user})

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response


def get_chatgpt_response(user_input):
    response = openai.ChatCompletion.create(
       model="gpt-4", 
       messages=[
            {"role": "system", "content": "Te egy hasznos asszisztens vagy."},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
    )
    return response.choices[0].message["content"]

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if user_message:
            response = get_chatgpt_response(user_message)
            return JsonResponse({'response': response})
        else:
            return JsonResponse({'error': 'Üzenet hiányzik'}, status=400)

    return JsonResponse({'error': 'Csak POST metódus engedélyezett'}, status=405)
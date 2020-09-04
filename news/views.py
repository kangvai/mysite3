from django.shortcuts import render
from .models import Post

# Create your views here.

def index(request):
    context = { 'news_list': Post.objects.all() }
    return render(request, 'news/index.html', context=context)
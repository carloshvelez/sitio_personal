from django.shortcuts import render
from datetime import datetime
from .models import Post, Project
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    last_posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    projects = Project.objects.all()
    context = {
        'last_posts': last_posts,
        'projects': projects
        
    }
    print(projects)
    return render(request, 'mi_sitio/index.html', context)

def post_display(request, slug):
    post = Post.objects.get(slug=slug)
    recent_posts = Post.objects.filter(status='published').exclude(slug=slug).order_by('-published_at')[:3]
    context = {
        'post': post,
        'recent_posts': recent_posts
    }
    print(context)
    return render(request, 'mi_sitio/post.html', context)

def blog(request):
    posts = Post.objects.filter(status='published').order_by('-published_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'mi_sitio/blog.html', context)

def em(request):
    return render(request,'mi_sitio/em.html')

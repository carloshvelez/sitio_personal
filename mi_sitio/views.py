from django.shortcuts import render
from datetime import datetime
from .models import Post, Project
from django.core.paginator import Paginator
import json
import requests
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from decouple import config

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

def assist(request):
    return render(request,'mi_sitio/assist.html')

def intervencion_breve(request):
    return render(request,'mi_sitio/intervencion_breve.html')

def libare(request):
    return render(request,'mi_sitio/libare.html')

def ccs(request):
    return render(request,'mi_sitio/ccs.html')

def michael_view(request):
    """View for the Michael Scott chatbot page"""
    return render(request, 'mi_sitio/michael.html')

@csrf_exempt
def michael_response(request):
    """API endpoint to get responses from DeepSeek for Michael Scott chatbot"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Prepare the prompt for DeepSeek
            prompt = f"""Eres Michael Scott de la serie de televisión The Office.
                Responde al siguiente mensaje con la voz y personalidad de Michael.
                Sé gracioso, a veces inapropiado, despistado pero con buenas intenciones.
                Usa las frases icónicas de Michael, cuando sea apropiado.
                Mantén las respuestas relativamente cortas (1-3 frases). No hagas referencias al lenguaje no verbal que el personaje está teniendo ahora mismo.
            
            User: {user_message}
            Michael Scott:"""
            
            # Call DeepSeek API
            deepseek_response = get_deepseek_response(prompt)
            
            return JsonResponse({'response': deepseek_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# Load environment variables from .env file


def get_deepseek_response(prompt):
    """Function to call DeepSeek API"""
    # Get API key from environment variables
  
    api_key = config('DEEPSEEK_API_KEY', default=False)
    
    if not api_key:
        print("Warning: DEEPSEEK_API_KEY not found in environment variables")
        # Proporcionar una respuesta de fallback en lugar de fallar
        return "¡Eso es lo que ella dijo! Parece que estoy teniendo problemas técnicos. Intenta más tarde."
    
    # API endpoint
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "deepseek-chat",  # Replace with the appropriate model name
        "messages": [
            {"role": "system", "content": "Eres Michael Scott, de la serie The Office."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        # Extract the response text based on DeepSeek's API response structure
        return result.get("choices", [{}])[0].get("message", {}).get("content", "¡Eso es lo que ella dijo!")
    except Exception as e:
        print(f"Error calling DeepSeek API: {e}")
        # Fallback response
        return "¡Eso es lo que ella dijo! Lo siento, estoy teniendo un pequeño bloqueo mental ahora mismo."

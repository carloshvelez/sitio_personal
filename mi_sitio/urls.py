from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'mi_sitio'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('em/', views.em, name='em'),
    path('post/<slug:slug>/', views.post_display, name='post_display')
]
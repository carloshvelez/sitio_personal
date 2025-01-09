from django.urls import path
from . import views

app_name = 'mi_sitio'
urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<slug:slug>/', views.post_display, name='post_display'),
    path('blog/', views.blog, name='blog'),
]
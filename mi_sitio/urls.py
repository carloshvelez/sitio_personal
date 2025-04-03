from django.contrib import admin
from django.urls import path
from . import views

app_name = 'mi_sitio' # Esto es para que Django sepa a qué aplicación pertenece cada URL en tu ap
urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('em/', views.em, name='em'),
    path('assist/', views.assist, name='assist'),
    path('libare', views.libare, name='libare'),
    path('ccs/', views.ccs, name='ccs'),
    path('intervencion_breve/', views.intervencion_breve, name='intervencion_breve'),
    path('post/<slug:slug>/', views.post_display, name='post_display'),
    path('michael/', views.michael_view, name='michael'),
    path('michael_response/', views.michael_response, name='michael_response'),
]
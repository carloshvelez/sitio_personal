from django.urls import path
from . import views

app_name = "empatia"
urlpatterns = [
    path("", views.index, name="index"),    
]
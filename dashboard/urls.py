from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
    path('api/summary-data/', views.get_summary_data, name='summary_data'),
]
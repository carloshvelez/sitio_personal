from django.contrib import admin
from .models import DashboardMetric, ActivityLog

@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'category', 'timestamp')
    list_filter = ('category', 'timestamp')
    search_fields = ('name', 'category')
    date_hierarchy = 'timestamp'

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'entity', 'status', 'created_at')
    list_filter = ('action', 'status', 'created_at')
    search_fields = ('user', 'entity', 'details')
    date_hierarchy = 'created_at'

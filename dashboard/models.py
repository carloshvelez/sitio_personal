from django.db import models

class DashboardMetric(models.Model):
    """Model to store dashboard metrics data"""
    name = models.CharField(max_length=100)
    value = models.FloatField()
    category = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Dashboard Metric"
        verbose_name_plural = "Dashboard Metrics"
        
    def __str__(self):
        return f"{self.name}: {self.value} ({self.category})"

class ActivityLog(models.Model):
    """Model to track user activity for the dashboard"""
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    user = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user} {self.action} {self.entity} ({self.status})"

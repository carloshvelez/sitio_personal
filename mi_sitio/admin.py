from django.contrib import admin
from .models import Post, Project, Technology
# Register your models here.

admin.site.register(Post)
admin.site.register(Project)
admin.site.register(Technology)

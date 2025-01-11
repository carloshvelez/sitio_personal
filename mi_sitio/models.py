from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
import markdown
from markdownx.models import MarkdownxField

# Create your models here.

STATUS_CHOICES = [
    ('draft', 'Borrador'),
    ('published', 'Publicado'),
    ('deleted', 'Eliminado'),
]

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="Carlos Humberto Vélez Ocampo")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image_url = models.CharField(max_length=500, default="/static/mi_sitio/images/default_post.webp")
    excerpt = models.TextField(blank=True, null=True)
    text = MarkdownxField("Contenido en MarkDown")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)    
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.status}"
    
    def publish(self):
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        #guardar asegurándonos de que el slug sea único
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_display', args=[self.slug])
    
    def text_html(self):
        return markdown.markdown(self.text, extensions=['extra', 'codehilite', 'toc'])

    
class Technology(models.Model):
    name = models.CharField(max_length=200)
    

    def __str__(self):
        return self.name
    

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=500, default="/static/mi_sitio/images/default_project.webp")
    technologies = models.ManyToManyField(Technology, related_name='projects')
    

    def __str__(self):
        return self.title

    
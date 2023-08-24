from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Blogs(BaseModel):
    STATUS_CHOICE = (
        ('draft',('DRAFT')),
        ('publish',('Publish')),
    )
    title = models.CharField(max_length=250, unique=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, null=True, blank=True)
    images = models.FileField(upload_to='attachments', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["-created_at"]
    
class Comments(BaseModel):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    comment = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.comment
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
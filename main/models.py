from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings

# Create your models here.
class StructuredProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published = models.DateTimeField("date published", default=datetime.now())
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class StructuredProjectContent(models.Model):
    slug = models.TextField()
    step = models.IntegerField()
    video_link = models.CharField(max_length=200)
    instructions = models.TextField()
    default_code = models.TextField()

    def __str__(self):
        return str(self.step)

class PersonalProject(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    code = models.TextField()

    def __str__(self):
        return self.title

class StructuredProjectCode(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    project = models.ForeignKey(StructuredProject, default=1, on_delete=models.CASCADE)
    code = models.TextField()
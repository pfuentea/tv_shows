from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Network(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Show(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateTimeField()
    network= models.ForeignKey(Network,  related_name="shows", on_delete = models.CASCADE)
    descr= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

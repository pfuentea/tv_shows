from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from datetime import date

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        today= date.today().strftime('%Y-%m-%d')
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['title']) < 2:
            errors["name"] = "El nombre del show debe tener al menos 5 caracteres"
        if postData['canales']=='otro':
            if len(postData['new_network']) < 3:
                errors["desc"] = "El nuevo Network debe ser de largo 3 o más"
        if postData['release_date'] > today:
            errors["release_date"] ="La fecha no debe ser superior a hoy"
        
        return errors

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if postData['password_confirm']!=postData['password']:
            errors["password"] = "Las contraseñas deben coincidir"
        return errors

# Create your models here.
class Network(models.Model):
    name = models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Show(models.Model):
    title = models.CharField(max_length=50,unique=True)
    release_date = models.DateTimeField()
    network= models.ForeignKey(Network,  related_name="shows", on_delete = models.CASCADE)
    descr= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager() 

class User(models.Model):
    name = models.CharField(max_length=255)
    email= models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    allowed= models.BooleanField(default =True)
    avatar = models.URLField(
        default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 

    def __repr__(self) -> str:
        return f'{self.id}:{self.name}'
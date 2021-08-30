
from django.shortcuts import render, HttpResponse,redirect
from .models import Show, Network, User
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import bcrypt
from .decorators import login_required


@login_required
def index(request):
    shows=Show.objects.all()
    logout='Logout'
    context = {
        "shows":shows,
        "logout":logout
    }
    return render(request, 'index.html', context)

# shows/<int:show_id>
@login_required
def detail(request,show_id):
    #messages.success(request,f'Usted va a visualizar un  TV Show ')
    show=Show.objects.get(id=show_id)
    context = {
        "show":show,    
    }
    return render(request, 'detail.html', context)

# shows/new
@login_required
def create(request):
    if request.method == "GET":
        canales = Network.objects.all()
        #messages.success(request,f'Usted va a crear un nuevo TV Show ')
        context = {
            "canales":canales,
        }
        return render(request, 'new.html', context)
    if request.method == "POST":
        errors = Show.objects.basic_validator(request.POST)
        if len(errors) > 0:
        # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
            for key, value in errors.items():
                messages.error(request, value)
            # redirigir al usuario al formulario para corregir los errores
            return redirect('/shows/create')
        else:
            titulo=request.POST['title']
            if request.POST['canales'] == 'otro':
                try:
                    canal=Network.objects.get(name=request.POST['new_network'])
                except ObjectDoesNotExist as DoesNotExist:
                    canal=Network.objects.create(name=request.POST['new_network'])
            else:
                canal=Network.objects.get(id=request.POST['canales'])        
            fecha=request.POST['release_date']
            descr=request.POST['description']
            Show.objects.create(title=titulo,network=canal,release_date=fecha,descr=descr)
            messages.success(request,f'Usted a creado un nuevo TV Show ')
            return redirect('/shows')

# shows/<int:show_id>/edit
@login_required
def edit(request,show_id):
    if request.method == "GET":
        show=Show.objects.get(id=show_id)
        fecha_lanzamiento=show.release_date
        fecha_lanzamiento=fecha_lanzamiento.strftime('%Y-%m-%d')
        print(fecha_lanzamiento)
        canales = Network.objects.all()
        context = {
            "show":show,
            "canales":canales,
            "fecha_lanzamiento":fecha_lanzamiento
        }
        return render(request, 'edit.html', context)
    if request.method == "POST":
        errors = Show.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirigir al usuario al formulario para corregir los errores
            return redirect('/shows/'+str(show_id)+'/edit')
        else:
            titulo=request.POST['title']          
            if request.POST['canales'] == 'otro':
                try:
                    canal=Network.objects.get(name=request.POST['new_network'])
                except ObjectDoesNotExist as DoesNotExist:
                    canal=Network.objects.create(name=request.POST['new_network'])
            else:
                canal=Network.objects.get(id=request.POST['canales'])            
            fecha=request.POST['release_date']
            descr=request.POST['description']        
            show=Show.objects.get(id=show_id)
            show.title=titulo
            show.network=canal
            show.release_date=fecha
            show.descr=descr
            show.save()
            messages.success(request,f'Se modificó el TV Show ')
            return redirect(f'/shows/{show_id}')
# shows/<int:show_id>/destroy
@login_required
def destroy(request,show_id):

    Show.objects.get(id=show_id).delete()
    #Show.objects.delete(target)
    messages.error(request,f'Usted a borrado el mejor programa de la historia ')
    shows=Show.objects.all()

    context = {
        "shows":shows
    }

    return redirect('/shows')

def test(request):
    context = {
    }

    return render(request, 'test.html', context)

def register(request):
    if request.method == "GET":
        context={}
        return render(request, 'register.html', context)
    if request.method == "POST":
        name=request.POST['name']
        email =request.POST['email']
        password=request.POST['password']
        #password_confirm= request.POST['email']

        errors= User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for k, mensaje_de_error in errors.items():
                messages.error(request,mensaje_de_error)
        
        else:
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            try:
                User.objects.create(name=name,email=email,password=pw_hash)
                return redirect('/shows')
            except IntegrityError :
                messages.error(request,'Este correo ya tiene un usuario.')
                return redirect('/register')

def login(request):
    email = request.POST['email']
    password=request.POST['password']
    try:
        user= User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/register')

    if not bcrypt.checkpw(password.encode(),user.password.encode()):
        messages.error(request,'Usuario inexistente o contraseña incorrecta')
        return redirect('/register')

    request.session['user']={
        'id':user.id,
        'name':user.name,
        'email':user.email,
        'avatar':user.avatar
    }
    return redirect('/shows')

def logout(request):
    request.session.clear()
    return redirect('/register')
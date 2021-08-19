
from django.shortcuts import render, HttpResponse,redirect
from .models import Show, Network
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    shows=Show.objects.all()
    context = {
        "shows":shows
    }
    return render(request, 'index.html', context)

# shows/<int:show_id>
def detail(request,show_id):
    #messages.success(request,f'Usted va a visualizar un  TV Show ')
    show=Show.objects.get(id=show_id)
    context = {
        "show":show,    
    }
    return render(request, 'detail.html', context)

# shows/new
def new(request):

    if request.method == "GET":
        canales = Network.objects.all()
        #messages.success(request,f'Usted va a crear un nuevo TV Show ')
        context = {
            "canales":canales,
        }
        return render(request, 'new.html', context)
    if request.method == "POST":
        titulo=request.POST['title']
        if request.POST['new_network'] != '':
            canal=Network.objects.get(id=request.POST['canales'])
        else:
            canal=Network.objects.create(name=request.POST['new_network'])
        
        fecha=request.POST['release_date']
        descr=request.POST['description']
        Show.objects.create(title=titulo,network=canal,release_date=fecha,descr=descr)
        messages.success(request,f'Usted a creado un nuevo TV Show ')
        return redirect('/shows')

# shows/<int:show_id>/edit
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
        return redirect('/shows')
# shows/<int:show_id>/destroy
def destroy(request,show_id):

    Show.objects.get(id=show_id).delete()
    #Show.objects.delete(target)
    messages.error(request,f'Usted a borrado el mejor programa de la historia ')
    shows=Show.objects.all()

    context = {
        "shows":shows
    }

    return redirect('/shows')
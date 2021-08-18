
from django.shortcuts import render, HttpResponse
from .models import Show, Network
from django.contrib import messages

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
    canales = Network.objects.all()
    
    #messages.success(request,f'Usted va a crear un nuevo TV Show ')
    context = {
        "canales":canales,
    }
    return render(request, 'new.html', context)

# shows/<int:show_id>/edit
def edit(request,show_id):
    show=Show.objects.get(id=show_id)
    context = {
        "show":show,    
    }
    return render(request, 'edit.html', context)

# shows/<int:show_id>/destroy
def destroy(request,show_id):
    Show.objects.delete(show_id)

    shows=Show.objects.all()
    context = {
        "shows":shows
    }
    return render(request, 'index.html', context)
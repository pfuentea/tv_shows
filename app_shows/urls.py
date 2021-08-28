from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('shows', views.index),
    path('shows/<int:show_id>', views.detail),
    path('shows/create', views.create), 
    path('shows/<int:show_id>/edit', views.edit),
    path('shows/<int:show_id>/destroy', views.destroy),
    path('shows/<int:show_id>/update', views.edit),
    path('test', views.test),
]

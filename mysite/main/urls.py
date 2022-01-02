from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check', views.validate, name='check'),
    path('Users', views.Users, name='Users'),
    path('add_user', views.add_user, name='add_user'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('edit_user', views.edit_user, name='delete_user'),
    path('ticket', views.ticket, name='ticket'),
    path('logout', views.logout, name='logout'),

    path('weight', views.weight, name='weight'),
]

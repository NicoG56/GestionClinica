from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('vista_recepcionista', views.recepcionista, name='vista_recepcionista'),
    path('vista_medico', views.medico, name='vista_medico'),
    path('vista_enfermera', views.enfermera, name='vista_enfermera'),
]
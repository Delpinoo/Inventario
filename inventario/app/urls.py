from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('eliminar-productos/', views.eliminar_productos, name='eliminar_productos'),
    path('modificar-producto/', views.modificar_producto, name='modificar_producto'),
    path('phones/', views.phones, name='phones'),
    path('modificar_telefono/<int:telefono_id>/', views.modificar_telefono, name='modificar_telefono'),
]
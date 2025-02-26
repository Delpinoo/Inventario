from django.urls import path
from app import views

urlpatterns = [
    path('', views.login_function, name="login"),
    path('home', views.home, name='home'),
    path('eliminar-productos/', views.eliminar_productos, name='eliminar_productos'),
    path('modificar_producto/', views.modificar_producto, name='modificar_producto'),
    path('phones/', views.phones, name='phones'),
    path('modificar_telefono/<int:telefono_id>/', views.modificar_telefono, name='modificar_telefono'),
    path('eliminar-telefonos/', views.eliminar_telefonos, name='eliminar_telefonos'),
    path('eliminar_telefonos/', views.eliminar_telefonos, name='eliminar_telefonos'),
    path("logout/", views.logout_function, name="logout"),
]   
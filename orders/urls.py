from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("change_Price", views.change_Price, name="change_Price"),
    path("cart", views.cart,name="cart"),
    path("realizar_pedido",views.realizar_pedido,name="realizar_pedido"),
    path("usuario", views.usuario_view, name="usuario_view")
]

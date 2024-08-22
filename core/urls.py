from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),  # Ruta para la página de inicio
    path("menu/", views.menu_list, name="menu_list"),
    path("menu/<int:item_id>/", views.menu_detail, name="menu_detail"),
    path(
        "categoria/<int:categoria_id>/",
        views.items_por_categoria,
        name="items_por_categoria",
    ),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("add_to_cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "remove_from_cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("process_order/", views.process_order, name="process_order"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    # Agrega más rutas aquí si es necesario
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_list, name="menu_list"),
    path("<int:item_id>/", views.menu_detail, name="menu_detail"),
    path(
        "categoria/<int:categoria_id>/",
        views.items_por_categoria,
        name="items_por_categoria",
    ),
    path(
        "add_to_cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"
    ),  # Ruta añadida
    path(
        "remove_from_cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("add_item/", views.add_menu_item, name="add_menu_item"),
    path("menu/delete/", views.delete_menu_item, name="delete_menu_item"),
    path("edit_item/<int:item_id>/", views.edit_menu_item, name="edit_menu_item"),
    path("search/", views.search, name="search"),
]

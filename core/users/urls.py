from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path(
        "logout/", LogoutView.as_view(next_page="home"), name="logout"
    ),  # Agregar logout
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("mis_pedidos/", views.mis_pedidos, name="mis_pedidos"),
    path("admin/panel_pedidos/", views.panel_pedidos, name="panel_pedidos"),
    path("update_estado/<int:order_id>/", views.update_estado, name="update_estado"),
]

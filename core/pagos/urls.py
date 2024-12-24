from django.urls import path
from . import views

urlpatterns = [
    path("process_order/", views.process_order, name="process_order"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path(
        "stripe-checkout/<int:order_id>/", views.stripe_checkout, name="stripe_checkout"
    ),
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),
]

from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, Order
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from core.pagos.utils import convert_to_brl
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


# Procesar pedido
def process_order(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(user=request.user)
    for item in cart.items.all():
        item.order = order
        item.save()
    cart.items.clear()
    return redirect(reverse("order_detail", args=[order.id]))


# Detalle del pedido
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "pagos/order_detail.html", {"order": order})


@login_required(
    login_url="/users/login/"
)  # Redirige a la vista de login si no está autenticado
def stripe_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Convertir el precio total de USD a BRL
    total_price_in_brl = convert_to_brl(order.get_total())

    try:
        # Crear la sesión de Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "brl",  # Cambiar la moneda a BRL
                        "product_data": {
                            "name": f"Pedido {order.id}",
                        },
                        "unit_amount": total_price_in_brl,  # Precio convertido en centavos
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=request.build_absolute_uri("/pagos/success/"),
            cancel_url=request.build_absolute_uri("/pagos/cancel/"),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        # Manejar errores
        return render(request, "pagos/error.html", {"error": str(e)})


def payment_success(request):
    return render(request, "pagos/success.html")


def payment_cancel(request):

    order = Order.objects.filter(user=request.user).last()
    return render(request, "pagos/cancel.html", {"order": order})

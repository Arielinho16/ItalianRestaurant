from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, OrderItem, Cart, Order, Categoria


# Vista para la página de inicio
def home(request):
    return render(request, "cuerpo_html/home.html")


def items_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    items = MenuItem.objects.filter(categoria=categoria)
    return render(
        request,
        "cuerpo_html/items_por_categoria.html",
        {"items": items, "categoria": categoria},
    )


# Función para mostrar el menú
def menu_list(request):
    items = MenuItem.objects.all()
    categorias = Categoria.objects.all()
    return render(
        request,
        "cuerpo_html/menu_list.html",
        {"items": items, "categorias": categorias},
    )


def menu_detail(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    return render(request, "cuerpo_html/menu_detail.html", {"item": item})


def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Crear o actualizar el OrderItem sin un Order asociado inicialmente
    order_item, created = OrderItem.objects.get_or_create(menu_item=item, order=None)

    if not created:
        order_item.quantity += 1
        order_item.save()

    cart.items.add(order_item)
    return redirect("cart_detail")


def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    order_item = get_object_or_404(OrderItem, id=item_id)

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        cart.items.remove(order_item)
        order_item.delete()

    return redirect("cart_detail")


def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = []
    total = 0

    for item in cart.items.all():
        item_total = item.menu_item.price * item.quantity
        total += item_total
        cart_items.append(
            {
                "item": item,
                "item_total": item_total,
            }
        )

    return render(
        request,
        "cuerpo_html/cart_detail.html",
        {"cart_items": cart_items, "total": total},
    )


# Función para procesar el pedido
def process_order(request):
    cart = Cart.objects.get(user=request.user)

    # Crear un nuevo Order para el usuario
    order = Order.objects.create(user=request.user)

    for item in cart.items.all():
        # Asociar cada OrderItem con el nuevo Order
        item.order = order
        item.save()
        order.items.add(item)

    # Vaciar el carrito después de procesar el pedido
    cart.items.clear()

    return redirect("order_detail", order_id=order.id)


# Función para mostrar los detalles de un pedido
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "cuerpo_html/order_detail.html", {"order": order})

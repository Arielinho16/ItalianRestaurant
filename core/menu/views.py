from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Categoria
from core.pagos.models import Cart, OrderItem
from .forms import MenuItemForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


# Lista de menú
def menu_list(request):
    items = MenuItem.objects.all()
    categorias = Categoria.objects.all()
    return render(
        request,
        "menu/menu_list.html",
        {"items": items, "categorias": categorias},
    )


# Buscador
def search(request):
    query = request.GET.get("q", "").strip()
    if query:
        # Buscar productos cuyo nombre contenga el query (insensible a mayúsculas/minúsculas)
        productos = MenuItem.objects.filter(name__icontains=query)
        # Buscar categorías cuyo nombre contenga el query
        categorias = Categoria.objects.filter(nombre__icontains=query)

        # Crear resultados en un formato JSON para devolver a la vista
        resultados = {
            "productos": [{"id": p.id, "name": p.name} for p in productos],
            "categorias": [{"id": c.id, "name": c.nombre} for c in categorias],
        }
        return JsonResponse(resultados)
    return JsonResponse({"productos": [], "categorias": []})


# Detalle de un elemento del menú
def menu_detail(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    return render(request, "menu/menu_detail.html", {"item": item})


# Filtrar por categoría
def items_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    items = MenuItem.objects.filter(categoria=categoria)
    return render(
        request,
        "items_por_categoria.html",
        {"items": items, "categoria": categoria},
    )


# Carrito de compras
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
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
        cart_items.append({"item": item, "item_total": item_total})
    return render(
        request,
        "menu/cart_detail.html",
        {"cart_items": cart_items, "total": total},
    )


@staff_member_required
def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)  # Manejar archivos subidos
        if form.is_valid():
            form.save()
            return redirect("menu_list")
    else:
        form = MenuItemForm()
    return render(request, "menu/add_menu_item.html", {"form": form})


@staff_member_required
def delete_menu_item(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        try:
            item = MenuItem.objects.get(name=item_name)
            item.delete()
            messages.success(request, f"El item '{item_name}' ha sido eliminado.")
        except MenuItem.DoesNotExist:
            messages.error(request, f"El item '{item_name}' no existe.")
    return redirect("menu_list")


@staff_member_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("menu_detail", item_id=item.id)
    else:
        form = MenuItemForm(instance=item)
    return render(request, "menu/edit_menu_item.html", {"form": form, "item": item})

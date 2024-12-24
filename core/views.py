from django.shortcuts import render, get_object_or_404, redirect
from core.menu.models import MenuItem, Categoria


# Vista para la página de inicio
def home(request):
    return render(request, "home.html")


def items_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    items = MenuItem.objects.filter(categoria=categoria)
    return render(
        request,
        "items_por_categoria.html",
        {"items": items, "categoria": categoria},
    )

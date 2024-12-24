from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from core.pagos.models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.admin.views.decorators import staff_member_required


# Registro de usuarios
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


# Perfil de usuario
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado con éxito!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)


@login_required
def mis_pedidos(request):
    pedidos = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "users/mis_pedidos.html", {"pedidos": pedidos})


@staff_member_required
def panel_pedidos(request):
    pedidos = {
        "en_preparacion": Order.objects.filter(estado="en_preparacion"),
        "enviado": Order.objects.filter(estado="enviado"),
        "entregado": Order.objects.filter(estado="entregado"),
    }
    return render(request, "pagos/panel_pedidos.html", {"pedidos": pedidos})


@staff_member_required
@csrf_exempt
def update_estado(request, order_id):
    if request.method == "POST":
        try:
            data = json.loads(
                request.body
            )  # Obtén los datos del cuerpo de la solicitud
            estado = data.get("estado")
            if not estado:
                return JsonResponse(
                    {"status": "error", "message": "Estado no proporcionado"},
                    status=400,
                )

            pedido = Order.objects.get(id=order_id)
            pedido.estado = estado
            pedido.save()
            return JsonResponse(
                {"status": "success", "message": "Estado actualizado correctamente"}
            )
        except Order.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Pedido no encontrado"}, status=404
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse(
        {"status": "error", "message": "Método no permitido"}, status=405
    )

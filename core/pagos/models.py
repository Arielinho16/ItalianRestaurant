from django.db import models
from django.contrib.auth.models import User
from core.menu.models import MenuItem
from decimal import Decimal


class Order(models.Model):
    ESTADOS = [
        ("en_preparacion", "En Preparación"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="en_preparacion")

    def __str__(self):
        return f"Order {self.id} by {self.user.username} ({self.get_estado_display()})"

    def get_total(self):
        total = sum(
            Decimal(item.menu_item.price) * Decimal(item.quantity)
            for item in self.items.all()
        )
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        total = sum(
            Decimal(item.menu_item.price) * Decimal(item.quantity)
            for item in self.items.all()
        )
        return total

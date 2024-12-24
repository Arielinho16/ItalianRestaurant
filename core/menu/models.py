from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(
        upload_to="menu_images/", blank=True, null=True
    )  # Cambiado a ImageField
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )

    def __str__(self):
        return self.name

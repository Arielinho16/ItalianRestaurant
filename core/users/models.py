from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        default="profile_pics/default_profile.jpg",  # Ruta relativa dentro de la carpeta MEDIA
        upload_to="profile_pics/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} Profile"

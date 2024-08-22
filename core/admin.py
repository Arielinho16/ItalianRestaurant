from django.contrib import admin
from .models import Categoria, MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    fields = ("name", "price", "description", "image_url", "categoria")
    list_display = ("name", "price", "description", "categoria")
    search_fields = ("name",)
    list_filter = ("price", "categoria")


admin.site.register(Categoria)
admin.site.register(MenuItem, MenuItemAdmin)

from django.contrib import admin
from .models import Papka, Fayl


@admin.register(Papka)
class PapkaAdmin(admin.ModelAdmin):
    list_display = ("nom", "foydalanuvchi", "ota_papka", "yaratilgan")
    list_filter = ("foydalanuvchi",)


@admin.register(Fayl)
class FaylAdmin(admin.ModelAdmin):
    list_display = ("nom", "foydalanuvchi", "papka", "hajm", "yangilangan")
    list_filter = ("foydalanuvchi",)

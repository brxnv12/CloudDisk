from django.urls import path
from . import views

app_name = "storage"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("papka/<int:papka_id>/", views.dashboard, name="papka"),
    path("yuklash/", views.fayl_yuklash, name="yuklash"),
    path("papka-yaratish/", views.papka_yaratish, name="papka_yaratish"),
    path("fayl/<int:fayl_id>/", views.fayl_korish, name="fayl_korish"),
    path("fayl/<int:fayl_id>/saqlash/", views.fayl_saqlash, name="fayl_saqlash"),
    path("fayl/<int:fayl_id>/ochirish/", views.fayl_ochirish, name="fayl_ochirish"),
    path("fayl/<int:fayl_id>/yuklab-olish/", views.fayl_yuklab_olish, name="fayl_yuklab_olish"),
    path("fayl/<int:fayl_id>/nom/", views.fayl_nomini_ozgartirish, name="fayl_nom"),
    path("papka/<int:papka_id>/ochirish/", views.papka_ochirish, name="papka_ochirish"),
]

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("royxatdan-otish/", views.royxatdan_otish, name="royxatdan_otish"),
    path("kirish/", views.kirish, name="kirish"),
    path("chiqish/", views.chiqish, name="chiqish"),
]

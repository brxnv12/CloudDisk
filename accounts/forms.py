from django import forms
from .models import User


class RoyxatdanOtishForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Masalan: Aziz Karimov", "autocomplete": "name"}),
        label="Ism va familiya",
        error_messages={"required": "Ism kiritilishi shart"},
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Masalan: aziz_99", "autocomplete": "username"}),
        label="Username",
        error_messages={"required": "Username kiritilishi shart"},
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "email@example.com (ixtiyoriy)", "autocomplete": "email"}),
        label="Email (ixtiyoriy)",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Kamida 6 ta belgi"}),
        label="Parol",
        min_length=6,
        error_messages={"required": "Parol kiritilishi shart", "min_length": "Parol kamida 6 ta belgi bo'lishi kerak"},
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Parolni qayta kiriting"}),
        label="Parolni tasdiqlash",
        error_messages={"required": "Parolni tasdiqlash shart"},
    )

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu username band, boshqa tanlang")
        if not username.replace("_", "").replace(".", "").isalnum():
            raise forms.ValidationError("Username faqat harf, raqam, _ va . dan iborat bo'lishi kerak")
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password_again")
        if p1 and p2 and p1 != p2:
            self.add_error("password_again", "Parollar mos kelmadi")
        return cleaned


class KirishForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username", "autocomplete": "username"}),
        label="Username",
        error_messages={"required": "Username kiritilishi shart"},
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Parol", "autocomplete": "current-password"}),
        label="Parol",
        error_messages={"required": "Parol kiritilishi shart"},
    )

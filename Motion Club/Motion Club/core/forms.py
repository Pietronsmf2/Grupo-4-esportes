from django import forms
from django.contrib.auth.hashers import make_password

from .models import Member


class MemberForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "Mínimo 6 caracteres"}),
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Repita a senha"}),
    )

    class Meta:
        model = Member
        fields = ["name", "email", "city", "level", "bio", "avatar", "favorite_sports"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nome completo"}),
            "email": forms.EmailInput(attrs={"placeholder": "voce@email.com"}),
            "city": forms.TextInput(attrs={"placeholder": "Cidade"}),
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "Conte um pouco sobre você…"}),
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/png", "class": "input-file"}),
            "favorite_sports": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shared CSS class on text-like fields (avatar = file input, styled apart).
        for name, field in self.fields.items():
            if name in ("favorite_sports", "avatar"):
                continue
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " input").strip()

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não conferem.")
        return cleaned

    def save(self, commit=True):
        member = super().save(commit=False)
        pwd = self.cleaned_data.get("password")
        if pwd:
            member.password = make_password(pwd)
        if commit:
            member.save()
            self.save_m2m()
        return member


class MemberEditForm(forms.ModelForm):
    """Editar o próprio perfil (sem senha, sem trocar e-mail)."""

    class Meta:
        model = Member
        fields = ["name", "city", "level", "bio", "avatar", "favorite_sports"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nome completo"}),
            "city": forms.TextInput(attrs={"placeholder": "Cidade"}),
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "Conte um pouco sobre você…"}),
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/png", "class": "input-file"}),
            "favorite_sports": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ("favorite_sports", "avatar"):
                continue
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " input").strip()

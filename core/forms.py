from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Submission

User = get_user_model()


# ---------------- CADASTRO DE USUÁRIO ----------------

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# ---------------- LOGIN ----------------

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)


# ---------------- FORMULÁRIO DE SUBMISSÃO ----------------

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["image", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

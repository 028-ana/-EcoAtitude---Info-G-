from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Submission, MATERIAL_CHOICES

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
    material_type = forms.ChoiceField(
        choices=MATERIAL_CHOICES,
        label="Tipo de Material",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    quantity = forms.DecimalField(
        max_value=9999.99,
        min_value=0.01,
        decimal_places=2,
        label="Quantidade (kg)",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0.01',
            'class': 'form-control',
            'placeholder': 'Ex: 2.50'
        })
    )

    class Meta:
        model = Submission
        fields = ["material_type", "quantity", "image", "description"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Descreva os materiais recicláveis..."
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control"
            })
        }
    
    def clean_quantity(self):
        """Validação customizada para o campo quantity"""
        quantity = self.cleaned_data.get('quantity')
        
        if quantity is None:
            raise forms.ValidationError("A quantidade é obrigatória.")
        
        if quantity <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        
        return quantity
    
    def clean_material_type(self):
        """Validação customizada para o campo material_type"""
        material_type = self.cleaned_data.get('material_type')
        
        if not material_type:
            raise forms.ValidationError("O tipo de material é obrigatório.")
        
        return material_type
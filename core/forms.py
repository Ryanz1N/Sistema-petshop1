from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from .models import Agendamento, Cliente, Pet, Venda
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nome', 'especie', 'raca', 'alertas']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'alertas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['pet', 'servico', 'data_inicio']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-select select2'}),
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
        }

class FuncionarioRegistroForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Nome", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    last_name = forms.CharField(required=True, label="Sobrenome", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}))
    email = forms.EmailField(required=True, label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nome@exemplo.com'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        # Adicionamos first_name e last_name na lista de campos
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# 2. Formulário de Login (Muda o label de Username para E-mail)
class EmailLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'E-mail',
        'autofocus': True
    }), label="E-mail") # Mudamos visualmente o rótulo
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Senha'
    }), label="Senha")
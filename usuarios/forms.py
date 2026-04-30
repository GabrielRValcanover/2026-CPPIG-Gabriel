from django import forms
from .models import Usuario

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'tipoUsuario', 'foto']

        error_messages = {
            'nome': {'required': 'O nome é um campo obrigatório'},
            'email': {'required': 'O email é um campo obrigatório'},
            'senha': {'required': 'A senha é um campo obrigatório'},
            'tipoUsuario': {'required': 'O tipo de usuário é um campo obrigatório'},
        }
from django import forms
from .models import UsuarioPersonalizado

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['nome','email','senha', 'tipoUsuario', 'foto']

        error_messages = {
            'nome': {'required': 'O username é um campo obrigatório'},
            'email': {'required': 'O email é um campo obrigatório'},
            'senha': {'required': 'A email é um campo obrigatório'},
            'tipoUsuario': {'required': 'O tipo de usuário é um campo obrigatório'},
        }
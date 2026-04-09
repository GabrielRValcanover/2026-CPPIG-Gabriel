from django import forms

from .models import Usuario

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O Nome do Usuario é um campo obrigatório'},
            'email': {'required': 'O email do Usuario é um campo obrigatório'},
            'senha': {'required': 'A Senha do Usuario é um campo obrigatório'},
            'TipoUsuario': {'required': 'Tipo do Usuario é um campo obrigatório'},
        }
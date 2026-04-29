from django import forms
from .models import CopiaChave


class CopiaChaveModelForm(forms.ModelForm):
    class Meta:
        model = CopiaChave
        fields = ['chave', 'identificador', 'status']

        error_messages = {
            'chave': {'required': 'A chave é um campo obrigatória'},
            'identificador': {'required': 'O identificador é um campo obrigatório'},
            'status': {'required': 'O status é um campo obrigatório'},
        }
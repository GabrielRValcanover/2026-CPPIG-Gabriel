from django import forms

from .models import Chave

class ChaveModelForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields =  ['descricao', 'status']

        error_messages = {
            'descricao': {'required': 'A do descricao é um campo obrigatório'},
            'status': {'required': 'O Status da chave é um campo obrigatório'},
        }
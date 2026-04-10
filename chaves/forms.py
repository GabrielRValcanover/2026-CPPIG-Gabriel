from django import forms

from .models import Chave

class ChaveModelForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = '__all__'

        error_messages = {
            'descricao': {'required': 'A do descricao é um campo obrigatório'},
            'codigo_indentificacao': {'required': 'O codigo da descrição é um campo obrigatório', 'unique': 'o Codigo já cadastrado'},
            'status': {'required': 'O Status da chave é um campo obrigatório'},
        }
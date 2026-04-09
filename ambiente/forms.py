from django import forms

from .models import Ambiente

class AmbienteModelForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O Nome do Ambiente é um campo obrigatório'},
            'nomenclatura': {'required': 'A nomenclatura do Ambiente é um campo obrigatório'},
            'exclusividade': {'required': 'A exclusividade do Ambiente é um campo obrigatório'},

        }

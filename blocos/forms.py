from django import forms

from .models import Bloco

class BlocoModelForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O Nome do Bloco é um campo obrigatório'},
            'quantidade': {'required': 'A quantidade do bloco é um campo obrigatório'},


        }

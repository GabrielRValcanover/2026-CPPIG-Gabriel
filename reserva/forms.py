from django import forms
from .models import Reserva
from chaves.models import Chave

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['pessoa', 'chaves', 'data_reserva', 'data_prevista', 'status']

        error_messages = {
            'pessoa': {'required': 'A pessoa é um campo obrigatório'},
            'chaves': {'required': 'Selecione ao menos uma chave'},
            'data_reserva': {'required': 'A data da reserva é um campo obrigatório'},
            'data_prevista': {'required': 'A data prevista é um campo obrigatório'},
            'status': {'required': 'O status é um campo obrigatório'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chaves'].queryset = Chave.objects.filter(
            status__in=['disponivel', 'reservada']
        )
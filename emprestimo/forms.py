from django import forms
from .models import Emprestimo
from copia_chave.models import CopiaChave

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['pessoa', 'copia_chave', 'entregue_por', 'data_prevista', 'hora', 'hora_prevista']

        error_messages = {
            'pessoa': {'required': 'A pessoa do emprestimo é um campo obrigatório'},
            'copia_chave': {'required': 'A cópia da chave do emprestimo é um campo obrigatório'},
            'entregue_por': {'required': 'Quem entregou a copia chave é um campo obrigatório'},
            'data_prevista': {'required': 'A data prevista do emprestimo é um campo obrigatório'},
            'hora': {'required': 'A hora de retirada do emprestimo é um campo obrigatório'},
            'hora_prevista': {'required': 'A hora prevista do emprestimo é um campo obrigatório'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['copia_chave'].queryset = CopiaChave.objects.all()
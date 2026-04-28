from django import forms

from .models import Emprestimo

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields =  ['pessoa', 'data_criacao','data_prevista','data_devolucao','status','hora' ]

        error_messages = {
            'pessoa': {'required': 'A pessoa é um campo obrigatório'},
            'data_criacao': {'required': 'A data de criação é um campo obrigatório'},
            'data_prevista': {'required': 'A data de prevista é um campo obrigatório'},
            'data_devolucao': {'required': 'A data de devolução é um campo obrigatório'},
            'status': {'required': 'O Status do emprestimo é um campo obrigatório'},
            'hora': {'required': 'A hora é um campo obrigatório'},
        }


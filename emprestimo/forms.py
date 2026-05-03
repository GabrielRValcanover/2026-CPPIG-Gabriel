from django import forms
from .models import Emprestimo
from copia_chave.models import CopiaChave
from usuarios.models import Usuario


class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['pessoa', 'copias_chave', 'entregue_por', 'data_prevista', 'hora', 'hora_prevista']

        error_messages = {
            'pessoa': {'required': 'A pessoa é um campo obrigatório'},
            'copias_chave': {'required': 'Selecione ao menos uma cópia de chave'},
            'entregue_por': {'required': 'Quem entregou é um campo obrigatório'},
            'data_prevista': {'required': 'A data prevista é um campo obrigatório'},
            'hora': {'required': 'A hora de retirada é um campo obrigatório'},
            'hora_prevista': {'required': 'A hora prevista é um campo obrigatório'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['copias_chave'].queryset = CopiaChave.objects.all()

        inspetores = Usuario.objects.filter(tipoUsuario='inspetor')
        if inspetores.exists():
            self.fields['entregue_por'].queryset = inspetores
        else:
            self.fields['entregue_por'].queryset = Usuario.objects.filter(tipoUsuario='secretaria')


class EmprestimoDevolucaoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['recebido_por', 'data_devolucao', 'hora_devolucao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        inspetores = Usuario.objects.filter(tipoUsuario='inspetor')
        if inspetores.exists():
            self.fields['recebido_por'].queryset = inspetores
        else:
            self.fields['recebido_por'].queryset = Usuario.objects.filter(tipoUsuario='secretaria')

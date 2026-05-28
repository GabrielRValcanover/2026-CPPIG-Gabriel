import self
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UsuarioPersonalizado

class UsuarioModelForm(forms.ModelForm):
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='Confirma senha', widget=forms.PasswordInput)
    class Meta:
        model = UsuarioPersonalizado
        fields = ['nome','email', 'senha', 'tipoUsuario', 'foto']
        error_messages = {
            'nome': {'required': 'O username é um campo obrigatório'},
            'email': {'required': 'O email é um campo obrigatório'},
            'senha': {'required': 'A email é um campo obrigatório'},
            'tipoUsuario': {'required': 'O tipo de usuário é um campo obrigatório'}
        }

#usei o raise para interromper e nao deixar salvar
    # def clean(self):
    #     cleaned_data = super().clean()
    #     senha = cleaned_data.get('senha')
    #     confirmar_senha = cleaned_data.get('confirmar_senha')
    #     if senha and confirmar_senha and senha != confirmar_senha:
    #         raise forms.ValidationError("senha nao correspondem")
    #     return cleaned_data

        # usei o raise para interromper e nao deixar salvar
        def clean(self):
            cleaned_data = super().clean()
            senha = cleaned_data.get('senha')
            confirmar_senha = cleaned_data.get('confirmar_senha')
            if senha and confirmar_senha and senha != confirmar_senha:
                raise forms.ValidationError('As senhas diferentes !')
            # verifica se já existe usuário com esse nome
            nome = cleaned_data.get('nome')
            if nome and UsuarioPersonalizado.objects.filter(username=nome).exists():
                raise forms.ValidationError(f'Já existe um usuário com o nome "{nome}".')

            return cleaned_data

    # tratamento do hash da senha
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data['nome']
        usuario.set_password(self.cleaned_data['senha'])
        if commit:
            usuario.save()
        return usuario


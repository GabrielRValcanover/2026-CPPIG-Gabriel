from django.db import models


class Usuario(models.Model):
    nome = models.CharField('Nome',max_length=70, help_text='Nome do usuario')
    email = models.CharField('Email',max_length=70, help_text='Email do usuario', unique=True)
    senha = models.CharField('Senha',max_length=70, help_text='senha do Fornecedor')
    tipoUsuario = models.CharField('tipoUsuario', max_length=70, help_text='Tipo do Usuario')

    class Meta:
         verbose_name = 'Usuario'
         verbose_name_plural = 'Usuarios'


    def __str__(self):
        return self.nome


from django.db import models
from stdimage import StdImageField

TIPO_CHOICES = [
  ('secretaria', 'Secretaria'),
  ('inspetor', 'Inspetor Escolar'),
  ('professor', 'Professor'),
]

class Usuario(models.Model):
    nome = models.CharField('Nome',max_length=70, help_text='Nome do usuario')
    email = models.CharField('Email',max_length=70, help_text='Email do usuario', unique=True)
    senha = models.CharField('Senha',max_length=70, help_text='senha do Fornecedor')
    tipoUsuario = models.CharField('tipoUsuario', max_length=70, choices=TIPO_CHOICES, default='secretaria')
    foto = StdImageField('Foto',upload_to='usuarios',delete_orphans=True, blank=True)
    class Meta:
         verbose_name = 'Usuario'
         verbose_name_plural = 'Usuarios'


    def __str__(self):
        return self.nome


class Secretaria(Usuario):
  class Meta:
    verbose_name = 'Secretaria'
    verbose_name_plural = 'Secretarias'


class InspesorEscolar(Usuario):
  class Meta:
    verbose_name = 'Inspetor Escolar'
    verbose_name_plural = 'Inspetores Escolares'


class Professor(Usuario):
  class Meta:
    verbose_name = 'Professor'
    verbose_name_plural = 'Professores'

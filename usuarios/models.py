from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from stdimage import StdImageField

TIPO_CHOICES = [
    ('secretaria', 'Secretaria'),
    ('inspetor', 'Inspetor'),
    ('professor', 'Professor'),
]

class UsuarioPersonalizado(AbstractUser):
    nome= models.CharField(verbose_name='Nome', max_length=70)
    tipoUsuario = models.CharField('Tipo de Usuário', max_length=70, choices=TIPO_CHOICES, default='secretaria')
    foto = StdImageField('Foto', upload_to='usuarios', delete_orphans=True, blank=True)
    bloqueado_ate = models.DateField('Bloqueado até', null=True, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.nome} ({self.tipoUsuario})"


class Secretaria(UsuarioPersonalizado):
    class Meta:
        proxy = True
        verbose_name = 'Secretaria'
        verbose_name_plural = 'Secretarias'

class Inspetor(UsuarioPersonalizado):
    class Meta:
        proxy = True
        verbose_name = 'Inspetor'
        verbose_name_plural = 'Inspetores'

class Professor(UsuarioPersonalizado):
    class Meta:
        proxy = True
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
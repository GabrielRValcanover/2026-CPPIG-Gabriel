from django.db import models
from ambiente.models import Ambiente

class Chave(models.Model):

    TIPO_CHOICES =[
      ('comum', 'Comum'),
      ('mestra', 'Mestra'),
    ]

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('manutencao', 'Manutenção'),
        ('perdida', 'Perdida'),
    ]
    descricao = models.CharField('Descrição:',max_length=70, help_text='Nome da Chave')
    status = models.CharField('Status',max_length=70, choices=STATUS_CHOICES)
    ambientes = models.ManyToManyField(Ambiente,related_name='chaves', blank=True)
    tipo = models.CharField('Tipo', max_length=20,choices=TIPO_CHOICES, default='comum')

    class Meta:
         verbose_name = 'Chave'
         verbose_name_plural = 'Chaves'

    def __str__(self):
           return self.descricao








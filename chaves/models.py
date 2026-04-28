from django.db import models
from ambiente.models import Ambiente

class Chave(models.Model):

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('manutencao', 'Manutenção'),
        ('perdida', 'Perdida'),
    ]
    descricao = models.CharField('Descrição:',max_length=70, help_text='Nome da Chave')
    status = models.CharField('Status',max_length=70, choices=STATUS_CHOICES)
    ambientes = models.ManyToManyField(Ambiente,related_name='chaves', blank=True)

    class Meta:
         verbose_name = 'Chave'
         verbose_name_plural = 'Chaves'

    def __str__(self):
           return self.descricao








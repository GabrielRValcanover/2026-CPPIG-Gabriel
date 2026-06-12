from django.db import models
from ambiente.models import Ambiente
from blocos.models import Bloco

class Chave(models.Model):

    TIPO_CHOICES =[
      ('comum', 'Comum'),
        ('mestraBloco', 'Mestra Bloco'),
      ('mestra', 'Mestra'),
    ]

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('manutencao', 'Manutenção'),
        ('perdida', 'Perdida'),
        ('danificada', 'Danificada'),
    ]
    descricao = models.CharField('Descrição:',max_length=70, help_text='Nome da Chave')
    status = models.CharField('Status',max_length=70, choices=STATUS_CHOICES)
    ambientes = models.ManyToManyField(Ambiente,related_name='chaves', blank=True)
    bloco = models.ForeignKey('blocos.Bloco',on_delete=models.CASCADE,null=True,blank=True,related_name='chaves')
    tipo = models.CharField('Tipo', max_length=20,choices=TIPO_CHOICES, default='comum')

    class Meta:
         verbose_name = 'Chave'
         verbose_name_plural = 'Chaves'

    def __str__(self):
           return self.descricao


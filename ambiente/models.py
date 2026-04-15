from ensurepip import bootstrap
from blocos.models import Bloco
from django.db import models

NOME_CHOICES = [
    ('sala', 'Sala'),
    ('bloco', 'Bloco'),
    ('cantina', 'Cantina'),
    ('sala_direcao', 'Sala Direcao'),
]

EXCLUSIVIDADE_CHOICES = [
    ('exclusivas', 'Exclusivas'),
    ('comunitarias', 'Comunitarias'),
]



class Ambiente(models.Model):
    nome = models.CharField('Nome',max_length=70,  choices=NOME_CHOICES)
    nomenclatura = models.CharField('nomenclatura',max_length=70, help_text='nomenclatura do ambiente')
    exclusividade = models.CharField('exclusividade', max_length=70, choices=EXCLUSIVIDADE_CHOICES)
    bloco = models.ForeignKey('blocos.Bloco', verbose_name='Bloco',
                              help_text='Nome do bloco', on_delete=models.CASCADE, related_name='ambientes',
                              null=True, blank=True)

    class Meta:
         verbose_name = 'Ambiente'
         verbose_name_plural = 'Ambientes'


    def __str__(self):
        return self.nome


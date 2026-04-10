from ensurepip import bootstrap

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

    class Meta:
         verbose_name = 'Ambiente'
         verbose_name_plural = 'Ambientes'


    def __str__(self):
        return self.nome


    def NOME_CHOICES(self):
        if NOME_CHOICES == 'sala':
            return bootstrap(Modal)
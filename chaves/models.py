from django.db import models


class Chave(models.Model):

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('manutencao', 'Manutenção'),
        ('perdida', 'Perdida'),
    ]
    descricao = models.CharField('Descrição:',max_length=70, help_text='Nome da Chave')
    status = models.CharField('Status',max_length=70, choices=STATUS_CHOICES)


    class Meta:
         verbose_name = 'Chave'
         verbose_name_plural = 'Chaves'


    def __str__(self):
        return self.descricao





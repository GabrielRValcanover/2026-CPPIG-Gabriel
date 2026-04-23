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
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, related_name='chaves',null=True, blank=True)
    bloco = models.ForeignKey('blocos.Bloco',on_delete=models.CASCADE,related_name='blocos',null=True,blank=True)

    class Meta:
         verbose_name = 'Chave'
         verbose_name_plural = 'Chaves'

    def __str__(self):
        if self.ambiente:
            return f"{self.descricao} - {self.ambiente.nomenclatura}"
        elif self.bloco:
            return f"{self.descricao} - Bloco {self.bloco}"
        return self.descricao






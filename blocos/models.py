from django.db import models


class Bloco(models.Model):

    nome = models.CharField('Nome', max_length=50, help_text='Nome do produto', unique=True)
    quantidade = models.IntegerField('Quantidade', help_text='Quantidade', max_length=20)


    class Meta:
         verbose_name = 'Bloco'
         verbose_name_plural = 'Blocos'


    def __str__(self):
        return self.nome




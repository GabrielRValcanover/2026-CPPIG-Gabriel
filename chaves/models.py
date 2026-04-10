from django.db import models


class Chave(models.Model):
    descricao = models.CharField('Descrição:',max_length=70, help_text='Nome da Chave')
    codigo_indentificacao = models.IntegerField('Codigo Indentificador',max_length=70, help_text='Codigo da Chave', unique=True)
    status = models.CharField('Status',max_length=70, help_text='Status do da chave')


    class Meta:
         verbose_name = 'Chave'
         verbose_name_plural = 'Chaves'


    def __str__(self):
        return self.descricao


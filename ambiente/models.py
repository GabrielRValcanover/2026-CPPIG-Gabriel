from django.db import models


class Ambiente(models.Model):
    nome = models.CharField('Nome',max_length=70, help_text='Nome do ambiente')
    nomenclatura = models.CharField('nomenclatura',max_length=70, help_text='nomenclatura do ambiente')
    exclusividade = models.CharField('exclusividade', max_length=70, help_text='exclusividade do ambiente')

    class Meta:
         verbose_name = 'Ambiente'
         verbose_name_plural = 'Ambientes'


    def __str__(self):
        return self.nome



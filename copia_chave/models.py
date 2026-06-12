from django.db import models


STATUS_CHOICES = [
    ('disponivel', 'Disponível'),
    ('emprestada', 'Emprestada'),
    ('reservada', 'Reservada'),
    ('manutencao', 'Manutenção'),
    ('perdida', 'Perdida'),
    ('danificada', 'Danificada'),
]


class CopiaChave(models.Model):
    chave = models.ForeignKey('chaves.Chave', verbose_name='Chave', help_text='Chave associada', on_delete=models.CASCADE, related_name='copias')
    identificador = models.CharField( max_length=50,verbose_name='Identificador',help_text='Identificador único da cópia',unique=True,null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    horario_devolucao= models.TimeField('hora de cada devolucao', null=True, blank=True)
    class Meta:
        verbose_name = 'Cópia de Chave'
        verbose_name_plural = 'Cópias de Chaves'

    def __str__(self):
      return f"{self.identificador} - {self.chave.descricao} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        codigoIndentificador = self._state.adding
        super().save(*args, **kwargs)
        if codigoIndentificador:
            CopiaChave.objects.filter(pk=self.pk).update(identificador=str(self.pk))
            self.identificador = str(self.pk)

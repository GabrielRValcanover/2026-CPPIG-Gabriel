from django.db import models


STATUS_CHOICES = [
    ('disponivel', 'Disponível'),
    ('emprestada', 'Emprestada'),
    ('reservada', 'Reservada'),
    ('manutencao', 'Manutenção'),
    ('perdida', 'Perdida'),
]


class CopiaChave(models.Model):
    chave = models.ForeignKey('chaves.Chave', verbose_name='Chave', help_text='Chave associada', on_delete=models.CASCADE, related_name='copias')
    identificador = models.CharField( max_length=50, verbose_name='Identificador',help_text='Identificador único da cópia', unique=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Cópia de Chave'
        verbose_name_plural = 'Cópias de Chaves'

    def __str__(self):
      return f"{self.identificador} - {self.chave.descricao} ({self.get_status_display()})"

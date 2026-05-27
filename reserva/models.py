from django.db import models
from django.conf import settings
from chaves.models import Chave

STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('confirmada', 'Confirmada'),
    ('cancelada', 'Cancelada'),
    ('concluida', 'Concluída'),
]

class Reserva(models.Model):
    pessoa = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Pessoa', on_delete=models.CASCADE, related_name='reservas')
    chaves = models.ManyToManyField(Chave, verbose_name='Chaves', related_name='reservas')
    data_reserva = models.DateField('Data da Reserva')
    datahora_prevista = models.DateTimeField('Data e hora Prevista de Uso')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"{self.pessoa.get_full_name() or self.pessoa.username} - {self.datahora_prevista}"

from django.db import models
from django.conf import settings
from copia_chave.models import CopiaChave

STATUS_CHOICES = [
    ('disponivel', 'Disponível'),
    ('emprestada', 'Emprestada'),
    ('reservada', 'Reservada'),
    ('manutencao', 'Manutenção'),
    ('danificada', 'Danificada'),
    ('perdida', 'Perdida'),
    ('devolvido', 'Devolvido'),

]


class Emprestimo(models.Model):
  pessoa = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Quem retirou', on_delete=models.CASCADE, related_name='emprestimos')
  entregue_por = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Entregue por', on_delete=models.SET_NULL, null=True,blank=True, related_name='emprestimos_entregues')
  recebido_por = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Recebido por', on_delete=models.SET_NULL, null=True,blank=True, related_name='emprestimos_recebidos')
  copias_chave = models.ManyToManyField(CopiaChave, verbose_name='Cópias das Chaves',related_name='emprestimos')
  data_criacao = models.DateField('Data Criação', auto_now_add=True)
  data_prevista = models.DateField('Data Prevista')
  data_devolucao = models.DateField('Data Devolução', null=True, blank=True)
  hora = models.TimeField('Hora de Retirada')
  hora_prevista = models.TimeField('Hora Prevista de Devolução')
  hora_devolucao = models.TimeField('Hora de Devolução', null=True, blank=True)
  status = models.CharField('Status', max_length=70, choices=STATUS_CHOICES)
  email_atraso = models.BooleanField(default=False)


  class Meta:
    verbose_name = 'Emprestimo'
    verbose_name_plural = 'Emprestimos'

  def __str__(self):
    return f"{self.pessoa.get_full_name() or self.pessoa.username} - {self.data_criacao}"








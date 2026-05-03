from django.db import models
from usuarios.models import Usuario
from copia_chave.models import CopiaChave

STATUS_CHOICES = [
    ('disponivel', 'Disponível'),
    ('emprestada', 'Emprestada'),
    ('reservada', 'Reservada'),
    ('manutencao', 'Manutenção'),
    ('perdida', 'Perdida'),
]


class Emprestimo(models.Model):
  pessoa = models.ForeignKey(Usuario, verbose_name='Quem retirou', on_delete=models.CASCADE, related_name='emprestimos')
  entregue_por = models.ForeignKey(Usuario, verbose_name='Entregue por', on_delete=models.SET_NULL, null=True,blank=True, related_name='emprestimos_entregues')
  recebido_por = models.ForeignKey(Usuario, verbose_name='Recebido por', on_delete=models.SET_NULL, null=True,blank=True, related_name='emprestimos_recebidos')
  copias_chave = models.ManyToManyField(CopiaChave, verbose_name='Cópias das Chaves',related_name='emprestimos')
  data_criacao = models.DateField('Data Criação', auto_now_add=True)
  data_prevista = models.DateField('Data Prevista')
  data_devolucao = models.DateField('Data Devolução', null=True, blank=True)
  hora = models.TimeField('Hora de Retirada')
  hora_prevista = models.TimeField('Hora Prevista de Devolução')
  hora_devolucao = models.TimeField('Hora de Devolução', null=True, blank=True)
  status = models.CharField('Status', max_length=70, choices=STATUS_CHOICES)

  class Meta:
    verbose_name = 'Emprestimo'
    verbose_name_plural = 'Emprestimos'

  def __str__(self):
    return f"{self.pessoa.nome} - {self.data_criacao}"








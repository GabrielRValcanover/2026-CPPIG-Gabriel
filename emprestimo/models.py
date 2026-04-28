from django.db import models

STATUS_CHOICES = [
    ('disponivel', 'Disponível'),
    ('emprestada', 'Emprestada'),
    ('reservada', 'Reservada'),
    ('manutencao', 'Manutenção'),
    ('perdida', 'Perdida'),
]

class Emprestimo(models.Model):
    pessoa = models.CharField('Pessoa', max_length=100)
    data_criacao = models.DateField('Data Criação', help_text='Data da criação do emprestimo')
    data_prevista = models.DateField('Data Prevista', help_text='Data da prevista do emprestimo')
    data_devolucao = models.DateField('Data Prevista', help_text='Data de Devolução do emprestimo')
    status = models.CharField('Status',max_length=70, choices=STATUS_CHOICES)
    hora = models.TimeField('Hora', help_text='Hora do emprestimo')


    class Meta:
         verbose_name = 'emprestimo'
         verbose_name_plural = 'emprestimos'

    def __str__(self):
           return self.pessoa








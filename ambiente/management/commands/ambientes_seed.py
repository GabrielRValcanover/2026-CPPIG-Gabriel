
from django.core.management.base import BaseCommand
from blocos.models import Bloco
from ambiente.models import Ambiente


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        blocos = Bloco.objects.all()

        Exclusividades_sala = ['exclusivas', 'comunitarias']

        for bloco in blocos:
            for i in range(1,bloco.quantidade +1):
                if i % 2 == 0:
                    exclusividade_sala = 'exclusivas'
                else:
                    exclusividade_sala = 'comunitarias'

                Ambiente.objects.create(
                    nome='sala',
                    nomenclatura=f' Sala{i}',
                    exclusividade=exclusividade_sala,
                    bloco=bloco
                )

        self.stdout.write(self.style.SUCCESS(f'Instâmcias de ambientes foram criadas com sucesso!'))


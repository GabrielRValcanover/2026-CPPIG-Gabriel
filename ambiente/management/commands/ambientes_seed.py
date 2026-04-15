from random import seed

from django.core.management.base import BaseCommand
from django_seed import Seed


from blocos.models import Bloco
from ambiente.models import Ambiente



class Command(BaseCommand):
    help = 'Seed customizado para gerar dados especificos para ambientes'


    def handle(self, *args, **Kwargs):
        blocos = Bloco.objects.all()
        for bloco in blocos:
            seeder= seeder.Seed(bloco)

            seeder.add_seed(bloco)

        self.stdout.write(self.style.SUCCESS(f'Instâmcias de ambientes foram criadas com sucesso!'))


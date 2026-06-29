import os
from django.apps import AppConfig


class EmprestimoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emprestimo'

    def ready(self):

        if os.environ.get('RUN_MAIN') == 'true':  #É uma verificação usada no Django para impedir que um bloco de código seja executado duas vezes durante o desenvolvimento local (Starck Overflow)
            from .jobs import start
            start()
            print('APPS READY EXECUTADO')
import os
from django.apps import AppConfig


class EmprestimoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emprestimo'

    def ready(self):

        if os.environ.get('RUN_MAIN') == 'true':
            from .jobs import start
            start()
            print('APPS READY EXECUTADO')
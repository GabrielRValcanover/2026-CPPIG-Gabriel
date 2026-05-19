from django.apps import AppConfig


class EmprestimoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emprestimo'

    def ready(self):
        from emprestimo.jobs import start
        start()


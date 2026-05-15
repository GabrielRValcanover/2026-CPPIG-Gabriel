from django.apps import AppConfig


class ReservaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reserva'

    def ready(self):
        from .utils.utils import start
        start()

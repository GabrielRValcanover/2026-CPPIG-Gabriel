from datetime import datetime, date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from reserva.models import Reserva


def cancelar_reserva(reserva):
    try:
        reserva = Reserva.objects.get(id=reserva_id,status='pendente')
        reserva.status = 'Cancelado'
        reserva.save()
    except Reserva.DoesNotExist:
        pass


def adiciona_job(reserva):
    cancelamento = reserva.datahora_prevista + timedelta(minutes=15)

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        cancelar_reserva,
        trigger='date',  # One-time execution
        run_date=cancelamento,  # Exact date/time to run
        id=reserva.id,  # Optional job ID,
        args=[reserva.id]
    )


def start():
    scheduler = BackgroundScheduler()
    scheduler.start()

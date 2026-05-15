
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def cancelar_reserva(reserva_id):
    from reserva.models import Reserva
    try:
        reserva = Reserva.objects.get(id=reserva_id, status='pendente')
        reserva.status = 'cancelada'
        reserva.save()
    except Reserva.DoesNotExist:
        pass

def adiciona_job(reserva):
    cancelamento = reserva.datahora_prevista + timedelta(minutes=15)
    scheduler.add_job(
        cancelar_reserva,
        trigger='date',
        run_date=cancelamento,
        id=str(reserva.id),
        args=[reserva.id]
    )

def start():
    if not scheduler.running:
        scheduler.start()
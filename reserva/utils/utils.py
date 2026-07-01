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
        replace_existing=True, # nao estava funcionando, por isso coloquei o replace(instrui o armazenamento de tarefas a sobrescrever uma tarefa com o mesmo ID) google
        args=[reserva.id]
    )

def start():
    if not scheduler.running:
        scheduler.start()
        print('tarefa de cancelar as reservas')
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def lembrete_email(emprestimo):

    from emprestimo.utils.utils import lembrete

    datahora_prevista = datetime.combine(
        emprestimo.data_prevista,
        emprestimo.hora_prevista
    )

    if emprestimo.pessoa.tipoUsuario == 'professor':
        horario_lembrete = (
            datahora_prevista - timedelta(days=1))
    else:
        horario_lembrete = (
            datahora_prevista - timedelta(seconds=10))
    scheduler.add_job(
        lembrete,
        trigger='date',
        run_date=horario_lembrete,
        id=f'lembrete_{emprestimo.id}',
        args=[emprestimo.id],
    )
def start():
    if not scheduler.running:
        scheduler.start()
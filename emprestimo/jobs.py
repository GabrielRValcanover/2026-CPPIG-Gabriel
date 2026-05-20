# from datetime import datetime, timedelta
#
# from apscheduler.schedulers.background import BackgroundScheduler
#
# scheduler = BackgroundScheduler()
#
#
# def lembrete_email(emprestimo):
#
#     from emprestimo.utils.utils import lembrete
#
#     datahora_prevista = datetime.combine(
#         emprestimo.data_prevista,
#         emprestimo.hora_prevista
#     )
#
#     if emprestimo.pessoa.tipoUsuario == 'professor':
#         horario_lembrete = (
#             datahora_prevista - timedelta(days=1))
#     else:
#         horario_lembrete = (
#             datahora_prevista - timedelta(seconds=10))
#     scheduler.add_job(
#         lembrete,
#         trigger='date',
#         run_date=horario_lembrete,
#         id=f'lembrete_{emprestimo.id}',
#         replace_existing=True,
#         args=[emprestimo.id],
#     )
# def start():
#     if not scheduler.running:
#         scheduler.start()

from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def lembrete_email(emprestimo):

    print('==========================')
    print('CRIANDO JOB DE LEMBRETE')
    print(f'Empréstimo ID: {emprestimo.id}')

    from emprestimo.utils.utils import lembrete

    datahora_prevista = datetime.combine(
        emprestimo.data_prevista,
        emprestimo.hora_prevista
    )

    print(f'Data/Hora prevista: {datahora_prevista}')

    if emprestimo.pessoa.tipoUsuario == 'professor':
        horario_lembrete = (
                datahora_prevista - timedelta(seconds=10))
    else:
        horario_lembrete = (
                datahora_prevista - timedelta(seconds=10)
        )

    print(f'Horário do lembrete: {horario_lembrete}')
    print(f'Horário atual: {datetime.now()}')

    scheduler.add_job(
        lembrete,
        trigger='date',
        run_date=horario_lembrete,
        id=f'lembrete_{emprestimo.id}',
        replace_existing=True,
        args=[emprestimo.id],
    )

    print('JOB CRIADO COM SUCESSO')
    print('==========================')


def start():
    if not scheduler.running:
        scheduler.start()
        print('SCHEDULER INICIADO')
from datetime import datetime, timedelta
from fastapi import APIRouter
from app.database import conectar

router = APIRouter()


@router.get("/desempenho-semanal")
def desempenho_semanal():
    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total_agendamentos,
               COALESCE(SUM(total), 0) AS faturamento_total
        FROM agendamentos
        WHERE data BETWEEN ? AND ?
          AND status != 'cancelado'
    """, (inicio_semana.isoformat(), fim_semana.isoformat()))
    resumo = dict(cursor.fetchone())

    cursor.execute("""
        SELECT COUNT(*) AS total_cancelados
        FROM agendamentos
        WHERE data BETWEEN ? AND ?
          AND status = 'cancelado'
    """, (inicio_semana.isoformat(), fim_semana.isoformat()))
    cancelados = dict(cursor.fetchone())

    cursor.execute("""
        SELECT s.nome, COUNT(*) AS quantidade
        FROM agendamento_servicos ags
        JOIN agendamentos a ON a.id = ags.agendamento_id
        JOIN servicos s ON s.id = ags.servico_id
        WHERE a.data BETWEEN ? AND ?
        GROUP BY s.nome
        ORDER BY quantidade DESC
    """, (inicio_semana.isoformat(), fim_semana.isoformat()))
    servicos = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "periodo": {
            "inicio": inicio_semana.isoformat(),
            "fim": fim_semana.isoformat()
        },
        "total_agendamentos": resumo["total_agendamentos"],
        "faturamento_total": resumo["faturamento_total"],
        "total_cancelados": cancelados["total_cancelados"],
        "servicos_mais_solicitados": servicos
    }
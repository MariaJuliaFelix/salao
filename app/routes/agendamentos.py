from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from app.database import conectar
from app.models.agendamentos import (
    AgendamentoCreate,
    AgendamentoUpdate,
    StatusAgendamentoUpdate,
    StatusServicoUpdate
)

router = APIRouter()

STATUS_VALIDOS_AGENDAMENTO = {"pendente", "confirmado", "cancelado", "concluido"}
STATUS_VALIDOS_SERVICO = {"pendente", "confirmado", "em_andamento", "concluido", "cancelado"}


def converter_para_minutos(horario: str) -> int:
    horas, minutos = map(int, horario.split(":"))
    return horas * 60 + minutos


def calcular_fim(horario: str, duracao: int) -> int:
    return converter_para_minutos(horario) + duracao


def datas_na_mesma_semana(data1: str, data2: str) -> bool:
    d1 = datetime.strptime(data1, "%Y-%m-%d")
    d2 = datetime.strptime(data2, "%Y-%m-%d")
    return d1.isocalendar()[1] == d2.isocalendar()[1] and d1.year == d2.year


def validar_horario_funcionamento(horario: str):
    minutos = converter_para_minutos(horario)
    inicio_funcionamento = 8 * 60
    fim_funcionamento = 18 * 60

    if minutos < inicio_funcionamento or minutos >= fim_funcionamento:
        raise HTTPException(
            status_code=400,
            detail="O salão funciona apenas entre 08:00 e 18:00"
        )


def obter_ou_criar_cliente(conn, nome_cliente: str):
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM clientes WHERE nome = ?", (nome_cliente,))
    cliente = cursor.fetchone()

    if cliente:
        return dict(cliente)

    cursor.execute("INSERT INTO clientes (nome) VALUES (?)", (nome_cliente,))
    conn.commit()

    return {"id": cursor.lastrowid, "nome": nome_cliente}


def buscar_servicos_por_ids(conn, servico_ids):
    cursor = conn.cursor()

    placeholders = ",".join(["?"] * len(servico_ids))
    cursor.execute(
        f"""
        SELECT id, nome, descricao, preco, duracao
        FROM servicos
        WHERE id IN ({placeholders})
        """,
        servico_ids
    )

    servicos = [dict(row) for row in cursor.fetchall()]

    if len(servicos) != len(servico_ids):
        raise HTTPException(status_code=404, detail="Um ou mais serviços não foram encontrados")

    return servicos


def calcular_total_e_duracao(servicos):
    total = sum(servico["preco"] for servico in servicos)
    duracao = sum(servico["duracao"] for servico in servicos)
    return total, duracao


def verificar_conflito(conn, data: str, horario: str, duracao: int, ignorar_agendamento_id=None):
    cursor = conn.cursor()

    if ignorar_agendamento_id is None:
        cursor.execute("""
            SELECT id, horario, duracao
            FROM agendamentos
            WHERE data = ? AND status != 'cancelado'
        """, (data,))
    else:
        cursor.execute("""
            SELECT id, horario, duracao
            FROM agendamentos
            WHERE data = ? AND status != 'cancelado' AND id != ?
        """, (data, ignorar_agendamento_id))

    agendamentos = cursor.fetchall()

    inicio_novo = converter_para_minutos(horario)
    fim_novo = inicio_novo + duracao

    for agendamento in agendamentos:
        inicio_existente = converter_para_minutos(agendamento["horario"])
        fim_existente = inicio_existente + agendamento["duracao"]

        if inicio_novo < fim_existente and fim_novo > inicio_existente:
            return True

    return False


def montar_agendamento_detalhado(conn, agendamento_id: int):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.id,
            c.nome AS cliente_nome,
            a.data,
            a.horario,
            a.total,
            a.duracao,
            a.status,
            a.observacao
        FROM agendamentos a
        JOIN clientes c ON c.id = a.cliente_id
        WHERE a.id = ?
    """, (agendamento_id,))

    agendamento = cursor.fetchone()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    cursor.execute("""
        SELECT
            s.id,
            s.nome,
            s.descricao,
            s.preco,
            s.duracao,
            ags.status
        FROM agendamento_servicos ags
        JOIN servicos s ON s.id = ags.servico_id
        WHERE ags.agendamento_id = ?
        ORDER BY s.nome
    """, (agendamento_id,))

    servicos = [dict(row) for row in cursor.fetchall()]

    resultado = dict(agendamento)
    resultado["servicos"] = servicos
    return resultado


@router.get("/disponibilidade")
def verificar_disponibilidade(data: str, horario: str, duracao: int = Query(..., gt=0)):
    validar_horario_funcionamento(horario)

    conn = conectar()
    conflito = verificar_conflito(conn, data, horario, duracao)
    conn.close()

    return {"disponivel": not conflito}


@router.post("/")
def criar_agendamento(agendamento: AgendamentoCreate):
    validar_horario_funcionamento(agendamento.horario)

    conn = conectar()

    cliente = obter_ou_criar_cliente(conn, agendamento.cliente_nome)
    servicos = buscar_servicos_por_ids(conn, agendamento.servicos)
    total, duracao = calcular_total_e_duracao(servicos)

    if verificar_conflito(conn, agendamento.data, agendamento.horario, duracao):
        conn.close()
        raise HTTPException(status_code=400, detail="Esse horário conflita com outro agendamento")

    sugestao_mesma_data = None
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.data
        FROM agendamentos a
        WHERE a.cliente_id = ?
        ORDER BY a.data DESC
    """, (cliente["id"],))

    agendamentos_cliente = cursor.fetchall()
    for item in agendamentos_cliente:
        if datas_na_mesma_semana(item["data"], agendamento.data):
            sugestao_mesma_data = item["data"]
            break

    cursor.execute("""
        INSERT INTO agendamentos (cliente_id, data, horario, total, duracao, status, observacao)
        VALUES (?, ?, ?, ?, ?, 'pendente', ?)
    """, (
        cliente["id"],
        agendamento.data,
        agendamento.horario,
        total,
        duracao,
        agendamento.observacao
    ))

    agendamento_id = cursor.lastrowid

    for servico in servicos:
        cursor.execute("""
            INSERT INTO agendamento_servicos (agendamento_id, servico_id, status)
            VALUES (?, ?, 'pendente')
        """, (agendamento_id, servico["id"]))

    conn.commit()

    resposta = montar_agendamento_detalhado(conn, agendamento_id)
    if sugestao_mesma_data:
        resposta["sugestao_mesma_data"] = sugestao_mesma_data

    conn.close()
    return resposta


@router.get("/")
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.id,
            c.nome AS cliente_nome,
            a.data,
            a.horario,
            a.total,
            a.duracao,
            a.status
        FROM agendamentos a
        JOIN clientes c ON c.id = a.cliente_id
        ORDER BY a.data, a.horario
    """)

    agendamentos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return agendamentos


@router.get("/historico")
def historico_agendamentos(data_inicio: str, data_fim: str):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id
        FROM agendamentos a
        WHERE a.data BETWEEN ? AND ?
        ORDER BY a.data, a.horario
    """, (data_inicio, data_fim))

    ids = [row["id"] for row in cursor.fetchall()]
    historico = [montar_agendamento_detalhado(conn, agendamento_id) for agendamento_id in ids]

    conn.close()
    return historico


@router.get("/{agendamento_id}")
def detalhar_agendamento(agendamento_id: int):
    conn = conectar()
    resultado = montar_agendamento_detalhado(conn, agendamento_id)
    conn.close()
    return resultado


@router.put("/{agendamento_id}")
def atualizar_agendamento(agendamento_id: int, dados: AgendamentoUpdate):
    validar_horario_funcionamento(dados.horario)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM agendamentos WHERE id = ?", (agendamento_id,))
    agendamento_atual = cursor.fetchone()

    if not agendamento_atual:
        conn.close()
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    data_agendada = datetime.strptime(agendamento_atual["data"], "%Y-%m-%d").date()
    hoje = datetime.now().date()

    if (data_agendada - hoje).days < 2:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Alterações online só podem ser feitas com pelo menos 2 dias de antecedência"
        )

    cliente = obter_ou_criar_cliente(conn, dados.cliente_nome)
    servicos = buscar_servicos_por_ids(conn, dados.servicos)
    total, duracao = calcular_total_e_duracao(servicos)

    if verificar_conflito(conn, dados.data, dados.horario, duracao, ignorar_agendamento_id=agendamento_id):
        conn.close()
        raise HTTPException(status_code=400, detail="Esse novo horário conflita com outro agendamento")

    cursor.execute("""
        UPDATE agendamentos
        SET cliente_id = ?, data = ?, horario = ?, total = ?, duracao = ?, observacao = ?
        WHERE id = ?
    """, (
        cliente["id"],
        dados.data,
        dados.horario,
        total,
        duracao,
        dados.observacao,
        agendamento_id
    ))

    cursor.execute("DELETE FROM agendamento_servicos WHERE agendamento_id = ?", (agendamento_id,))

    for servico in servicos:
        cursor.execute("""
            INSERT INTO agendamento_servicos (agendamento_id, servico_id, status)
            VALUES (?, ?, 'pendente')
        """, (agendamento_id, servico["id"]))

    conn.commit()

    resposta = montar_agendamento_detalhado(conn, agendamento_id)
    conn.close()
    return resposta


@router.patch("/{agendamento_id}/confirmar")
def confirmar_agendamento(agendamento_id: int):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM agendamentos WHERE id = ?", (agendamento_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    cursor.execute("""
        UPDATE agendamentos
        SET status = 'confirmado'
        WHERE id = ?
    """, (agendamento_id,))
    conn.commit()

    resposta = montar_agendamento_detalhado(conn, agendamento_id)
    conn.close()
    return resposta


@router.patch("/{agendamento_id}/status")
def atualizar_status_agendamento(agendamento_id: int, dados: StatusAgendamentoUpdate):
    if dados.status not in STATUS_VALIDOS_AGENDAMENTO:
        raise HTTPException(status_code=400, detail="Status de agendamento inválido")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM agendamentos WHERE id = ?", (agendamento_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    cursor.execute("""
        UPDATE agendamentos
        SET status = ?
        WHERE id = ?
    """, (dados.status, agendamento_id))
    conn.commit()

    resposta = montar_agendamento_detalhado(conn, agendamento_id)
    conn.close()
    return resposta


@router.patch("/{agendamento_id}/servicos/{servico_id}/status")
def atualizar_status_servico(agendamento_id: int, servico_id: int, dados: StatusServicoUpdate):
    if dados.status not in STATUS_VALIDOS_SERVICO:
        raise HTTPException(status_code=400, detail="Status de serviço inválido")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM agendamento_servicos
        WHERE agendamento_id = ? AND servico_id = ?
    """, (agendamento_id, servico_id))

    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Serviço não encontrado nesse agendamento")

    cursor.execute("""
        UPDATE agendamento_servicos
        SET status = ?
        WHERE agendamento_id = ? AND servico_id = ?
    """, (dados.status, agendamento_id, servico_id))
    conn.commit()

    resposta = montar_agendamento_detalhado(conn, agendamento_id)
    conn.close()
    return resposta
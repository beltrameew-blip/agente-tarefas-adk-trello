"""Ferramentas determinísticas do agente ADK para o Trello.

Nenhuma credencial é registrada ou enviada para o modelo. A conexão é criada
somente durante a chamada de uma ferramenta; testes podem substituí-la.
"""

from __future__ import annotations

import os
import unicodedata
from datetime import date, datetime, time
from zoneinfo import ZoneInfo


STATUS_CANONICO = {"a fazer": "A fazer", "em andamento": "Em andamento", "concluido": "Concluído"}
ALIAS_STATUS = {
    "a fazer": "a fazer", "afazer": "a fazer", "to do": "a fazer", "todo": "a fazer",
    "em andamento": "em andamento", "andamento": "em andamento", "fazendo": "em andamento", "doing": "em andamento",
    "concluido": "concluido", "concluida": "concluido", "concluidos": "concluido", "concluidas": "concluido",
    "finalizado": "concluido", "finalizada": "concluido", "feito": "concluido", "done": "concluido",
}


def _limpar(texto: str) -> str:
    """Normaliza espaços, acentuação e letras para comparações robustas."""
    base = unicodedata.normalize("NFKD", str(texto or ""))
    base = "".join(c for c in base if not unicodedata.combining(c))
    return " ".join(base.casefold().split())


def _status(texto: str) -> str:
    chave = ALIAS_STATUS.get(_limpar(texto))
    if not chave:
        raise ValueError("Status inválido. Use: A fazer, Em andamento ou Concluído.")
    return chave


def _agora() -> datetime:
    fuso = os.getenv("APP_TIMEZONE", "America/Sao_Paulo")
    return datetime.now(ZoneInfo(fuso))


def get_temporal_context() -> dict:
    """Retorna data e hora atuais no fuso horário configurado para organizar tarefas."""
    try:
        agora = _agora()
        return {"status": "sucesso", "data_hoje": agora.date().isoformat(),
                "data_hora": agora.isoformat(timespec="seconds"), "fuso": os.getenv("APP_TIMEZONE", "America/Sao_Paulo")}
    except Exception:
        return {"status": "erro", "mensagem": "Fuso horário inválido. Confira APP_TIMEZONE."}


def _data_para_trello(data_vencimento: str) -> str:
    """Usa meio-dia local com offset, evitando conversões UTC para a véspera.

    Contrato: data YYYY-MM-DD, sem horário; o Trello representa due como datetime.
    Meio-dia é uma convenção explícita de apresentação, não prazo às 23:59.
    """
    try:
        dia = date.fromisoformat(data_vencimento)
        if dia.isoformat() != data_vencimento:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Data inválida. Informe exatamente AAAA-MM-DD (ex.: 2026-11-12).") from None
    return datetime.combine(dia, time(12, 0), tzinfo=ZoneInfo(os.getenv("APP_TIMEZONE", "America/Sao_Paulo"))).isoformat()


def _cliente():
    chave = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    if not chave or not token:
        raise RuntimeError("Credenciais Trello ausentes. Preencha TRELLO_API_KEY e TRELLO_TOKEN no .env.")
    from trello import TrelloClient  # import tardio: testes offline não precisam de py-trello
    return TrelloClient(api_key=chave, api_secret=os.getenv("TRELLO_API_SECRET") or None, token=token)


def _quadro():
    quadros = _cliente().list_boards()
    id_quadro = os.getenv("TRELLO_BOARD_ID", "").strip()
    nome = _limpar(os.getenv("TRELLO_BOARD_NAME", "DIO"))
    encontrados = [q for q in quadros if (q.id == id_quadro if id_quadro else _limpar(q.name) == nome)]
    if len(encontrados) == 0:
        raise LookupError("Quadro Trello não encontrado. Confira TRELLO_BOARD_NAME ou TRELLO_BOARD_ID.")
    if len(encontrados) > 1:
        raise LookupError("Mais de um quadro com esse nome. Configure TRELLO_BOARD_ID para escolher um único.")
    return encontrados[0]


def _listas(quadro):
    resultado = {}
    for lista in quadro.list_lists():
        tipo = ALIAS_STATUS.get(_limpar(lista.name))
        if tipo and tipo not in resultado:
            resultado[tipo] = lista
    return resultado


def _erro(exc: Exception) -> dict:
    """Não propaga exceções brutas que podem conter dados sensíveis."""
    if isinstance(exc, (ValueError, LookupError)):
        mensagem = str(exc)
    elif isinstance(exc, RuntimeError) and str(exc).startswith("Credenciais Trello ausentes"):
        mensagem = str(exc)
    else:
        mensagem = "Falha ao acessar o Trello. Verifique conexão, autorização e configurações."
    return {"status": "erro", "mensagem": mensagem}


def adicionar_tarefa(nome_da_tarefa: str, descricao_da_tarefa: str, data_vencimento: str) -> dict:
    """Cria um cartão na lista 'A fazer'. Data obrigatória em AAAA-MM-DD."""
    try:
        nome = str(nome_da_tarefa or "").strip()
        if not nome or len(nome) > 160:
            raise ValueError("O nome da tarefa é obrigatório e deve ter até 160 caracteres.")
        if len(str(descricao_da_tarefa or "")) > 5000:
            raise ValueError("Descrição muito longa (limite demonstrativo: 5000 caracteres).")
        due = _data_para_trello(data_vencimento)
        listas = _listas(_quadro())
        if "a fazer" not in listas:
            raise LookupError("Lista 'A fazer' não encontrada. Crie as listas A fazer, Em andamento e Concluído.")
        cartao = listas["a fazer"].add_card(name=nome, desc=str(descricao_da_tarefa or ""), due=due)
        return {"status": "sucesso", "acao": "criada", "id": str(cartao.id), "nome": nome,
                "status_tarefa": "A fazer", "data_vencimento": data_vencimento}
    except Exception as exc:
        return _erro(exc)


def listar_tarefas(status: str = "todas") -> dict:
    """Lista cartões do quadro, opcionalmente filtrando por status."""
    try:
        filtro = None if _limpar(status) in ("todas", "todos", "") else _status(status)
        listas = _listas(_quadro())
        if filtro and filtro not in listas:
            raise LookupError(f"Lista '{STATUS_CANONICO[filtro]}' não encontrada no quadro.")
        tarefas = []
        for chave, lista in listas.items():
            if filtro and chave != filtro:
                continue
            for cartao in lista.list_cards():
                vencimento = getattr(cartao, "due", None)
                if isinstance(vencimento, (date, datetime)):
                    vencimento = vencimento.isoformat()
                tarefas.append({"id": str(cartao.id), "nome": cartao.name, "descricao": cartao.desc or "",
                                "vencimento": vencimento, "status_tarefa": STATUS_CANONICO[chave]})
        return {"status": "sucesso", "total": len(tarefas), "tarefas": tarefas}
    except Exception as exc:
        return _erro(exc)


def mudar_status_tarefa(nome_da_tarefa: str, novo_status: str) -> dict:
    """Move um cartão com nome exato para A fazer, Em andamento ou Concluído.

    Rejeita nomes ambíguos para não alterar a tarefa errada.
    """
    try:
        nome = _limpar(nome_da_tarefa)
        if not nome:
            raise ValueError("Informe o nome da tarefa que deseja mover.")
        chave_destino = _status(novo_status)
        listas = _listas(_quadro())
        if chave_destino not in listas:
            raise LookupError(f"Lista '{STATUS_CANONICO[chave_destino]}' não encontrada no quadro.")
        encontrados = [(chave, cartao) for chave, lista in listas.items()
                       for cartao in lista.list_cards() if _limpar(cartao.name) == nome]
        if not encontrados:
            raise LookupError("Tarefa não encontrada. Use listar_tarefas para conferir o nome exato.")
        if len(encontrados) > 1:
            raise ValueError("Há tarefas com nomes iguais. Renomeie ou diferencie os cartões antes de mover.")
        origem, cartao = encontrados[0]
        if origem == chave_destino:
            return {"status": "sucesso", "acao": "sem_alteracao", "nome": cartao.name,
                    "status_tarefa": STATUS_CANONICO[chave_destino]}
        cartao.change_list(listas[chave_destino].id)
        return {"status": "sucesso", "acao": "movida", "nome": cartao.name,
                "de": STATUS_CANONICO[origem], "para": STATUS_CANONICO[chave_destino], "id": str(cartao.id)}
    except Exception as exc:
        return _erro(exc)

"""Teste local opcional de conexão Gemini/Trello; --completo cria e move um único cartão de teste.

Não coleta, registra nem imprime credenciais. Requer .env preenchido LOCALMENTE.
O resultado só comprova os serviços aqui testados, não substitui o ADK Web.
"""
import argparse
import os
import sys
import importlib.util
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / "adk_tarefas" / ".env")
spec = importlib.util.spec_from_file_location("ferramentas_validacao", ROOT / "adk_tarefas" / "tools.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)


def valida_credenciais():
    chaves = ("GOOGLE_API_KEY", "TRELLO_API_KEY", "TRELLO_TOKEN")
    ausentes = [k for k in chaves if not os.getenv(k) or os.getenv(k, "").startswith(("COLE_", "SUA_"))]
    if ausentes:
        raise RuntimeError("Complete as credenciais no arquivo local adk_tarefas/.env: " + ", ".join(ausentes))


def gemini_teste():
    from google import genai
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    try:
        resposta = client.models.generate_content(model=modelo, contents="Responda somente OK.")
        if not getattr(resposta, "text", None):
            raise RuntimeError("Sem resposta do modelo")
    finally:
        client.close()
    print("[OK] Gemini respondeu à chamada de teste (uso sujeito à cota da API).")


def trello_teste(completo=False):
    resultado = tools.listar_tarefas("todas")
    if resultado.get("status") != "sucesso":
        raise RuntimeError("Trello: " + resultado.get("mensagem", "sem resposta"))
    print("[OK] Trello acessível, quadro e listas consultados. Cartões encontrados:", resultado["total"])
    if not completo:
        return
    nome = "DIO VALIDACAO " + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:6]
    prazo = (datetime.now(tools.ZoneInfo(os.getenv("APP_TIMEZONE", "America/Sao_Paulo"))) + timedelta(days=1)).date().isoformat()
    print("[AVISO] Será criado e mantido um cartão de teste com prefixo DIO VALIDACAO.")
    criado = tools.adicionar_tarefa(nome, "Validação automática de criar, listar e movimentar", prazo)
    if criado.get("status") != "sucesso":
        raise RuntimeError("Criar cartão: " + criado.get("mensagem", "falha"))
    print("[OK] Criação em A fazer.")
    r = tools.listar_tarefas("A fazer")
    if r.get("status") != "sucesso" or nome not in [c["nome"] for c in r.get("tarefas", [])]:
        raise RuntimeError("Cartão não apareceu na lista A fazer")
    print("[OK] Cartão encontrado em A fazer.")
    for destino in ("Em andamento", "Concluído"):
        m = tools.mudar_status_tarefa(nome, destino)
        if m.get("status") != "sucesso":
            raise RuntimeError("Mover cartão: " + m.get("mensagem", "falha"))
        r = tools.listar_tarefas(destino)
        if r.get("status") != "sucesso" or nome not in [c["nome"] for c in r.get("tarefas", [])]:
            raise RuntimeError("Cartão não encontrado após mover para " + destino)
        print("[OK] Movido e encontrado em", destino)
    print("[OK] Teste Trello completo. Cartão permanece em Concluído. Nome:", nome)



def main():
    parser = argparse.ArgumentParser(description="Valida Google Gemini e conexão real ao quadro Trello")
    parser.add_argument("--completo", action="store_true", help="Cria um cartão de teste e o move entre listas no Trello")
    args = parser.parse_args()
    try:
        valida_credenciais()
        gemini_teste()
        trello_teste(completo=args.completo)
    except Exception as exc:
        # Não expor detalhes de exceções de SDK/API que possam conter tokens.
        if isinstance(exc, RuntimeError) and (str(exc).startswith(("Complete", "Trello:", "Criar", "Mover", "Cartão", "Listagem"))):
            print("[ERRO]", exc)
        else:
            print("[ERRO] Falha na validação. Confirme chaves, acesso aos serviços, cotas e conectividade.")
        return 1
    print("[OK] Validação finalizada. Confirme agora o agente no ADK Web.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

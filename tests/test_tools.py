"""Testes determinísticos: nenhum token, chamada externa ou modelo de IA exigido."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

CAMINHO = Path(__file__).resolve().parents[1] / "adk_tarefas" / "tools.py"
spec = importlib.util.spec_from_file_location("ferramentas_offline", CAMINHO)
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
_CLIENTE_ORIGINAL = tools._cliente


class Cartao:
    def __init__(self, nome, descricao="", due=None, id_="c1"):
        self.id, self.name, self.desc, self.due = id_, nome, descricao, due
        self.moves = []

    def change_list(self, list_id):
        self.moves.append(list_id)


class Lista:
    def __init__(self, nome, id_):
        self.name, self.id, self.cards = nome, id_, []

    def add_card(self, name, desc, due):
        novo = Cartao(name, desc, due, "novo-123")
        self.cards.append(novo)
        return novo

    def list_cards(self):
        return list(self.cards)


class Quadro:
    def __init__(self, listas=None, nome="DIO", id_="q1"):
        self.name, self.id = nome, id_
        self.listas = listas or [Lista("A fazer", "l1"), Lista("Em andamento", "l2"), Lista("Concluído", "l3")]

    def list_lists(self):
        return self.listas


class Cliente:
    def __init__(self, quadros):
        self.quadros = quadros

    def list_boards(self):
        return self.quadros


class TestesFerramentas(unittest.TestCase):
    def setUp(self):
        self.quadro = Quadro()
        self.patcher = patch.object(tools, "_cliente", return_value=Cliente([self.quadro]))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.env = patch.dict(os.environ, {"TRELLO_BOARD_NAME": "DIO", "TRELLO_BOARD_ID": "", "APP_TIMEZONE": "America/Sao_Paulo"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_hora_temporal_tem_fuso(self):
        r = tools.get_temporal_context()
        self.assertEqual(r["status"], "sucesso")
        self.assertEqual(len(r["data_hoje"]), 10)
        self.assertEqual(r["fuso"], "America/Sao_Paulo")

    def test_data_sem_atraso_utc(self):
        self.assertEqual(tools._data_para_trello("2026-11-12"), "2026-11-12T12:00:00-03:00")

    def test_data_invalida_foi_rejeitada(self):
        r = tools.adicionar_tarefa("Estudar", "", "12/11/2026")
        self.assertEqual(r["status"], "erro")
        self.assertIn("AAAA-MM-DD", r["mensagem"])

    def test_cria_tarefa(self):
        r = tools.adicionar_tarefa("Revisar Python", "Estudar funções", "2026-11-12")
        self.assertEqual(r["status"], "sucesso")
        self.assertEqual(r["data_vencimento"], "2026-11-12")
        self.assertEqual(self.quadro.listas[0].cards[0].name, "Revisar Python")
        self.assertEqual(self.quadro.listas[0].cards[0].due[-6:], "-03:00")

    def test_cria_nome_em_branco_rejeitado(self):
        self.assertEqual(tools.adicionar_tarefa("  ", "desc", "2026-11-12")["status"], "erro")

    def test_lista_por_status_e_todas(self):
        self.quadro.listas[0].cards.append(Cartao("Nova"))
        self.quadro.listas[2].cards.append(Cartao("Final", id_="c2"))
        self.assertEqual(tools.listar_tarefas("todas")["total"], 2)
        self.assertEqual(tools.listar_tarefas("concluido")["total"], 1)
        self.assertEqual(tools.listar_tarefas("concluído")["tarefas"][0]["nome"], "Final")

    def test_status_com_acentuacao_e_espacos(self):
        self.quadro.listas[0].cards.append(Cartao("Revisar   PYTHON"))
        r = tools.mudar_status_tarefa(" revisar python ", "CONCLUÍDO")
        self.assertEqual(r["status"], "sucesso")
        self.assertEqual(r["para"], "Concluído")
        self.assertEqual(self.quadro.listas[0].cards[0].moves, ["l3"])

    def test_movimento_repetido_sem_efeitos(self):
        self.quadro.listas[2].cards.append(Cartao("Revisar"))
        r = tools.mudar_status_tarefa("Revisar", "feito")
        self.assertEqual(r["acao"], "sem_alteracao")
        self.assertEqual(self.quadro.listas[2].cards[0].moves, [])

    def test_tarefa_duplicada_nao_move(self):
        for lista in self.quadro.listas[:2]:
            lista.cards.append(Cartao("Igual"))
        r = tools.mudar_status_tarefa("Igual", "concluido")
        self.assertEqual(r["status"], "erro")
        self.assertIn("nomes iguais", r["mensagem"])
        self.assertEqual(self.quadro.listas[0].cards[0].moves, [])

    def test_tarefa_inexistente(self):
        self.assertEqual(tools.mudar_status_tarefa("Ausente", "concluido")["status"], "erro")

    def test_status_invalido_nao_lista_tudo(self):
        self.quadro.listas[0].cards.append(Cartao("Teste"))
        self.assertEqual(tools.listar_tarefas("talvez")["status"], "erro")

    def test_quadro_ausente(self):
        with patch.object(tools, "_cliente", return_value=Cliente([])):
            self.assertIn("não encontrado", tools.listar_tarefas()["mensagem"])

    def test_quadro_duplicado_precisa_id(self):
        with patch.object(tools, "_cliente", return_value=Cliente([self.quadro, Quadro(id_="q2")])):
            self.assertIn("TRELLO_BOARD_ID", tools.listar_tarefas()["mensagem"])

    def test_erro_de_conexao_nao_revela_token(self):
        with patch.object(tools, "_cliente", side_effect=RuntimeError("Meu token secreto 123")):
            r = tools.listar_tarefas()
            self.assertEqual(r["status"], "erro")
            self.assertNotIn("token secreto", str(r))

    def test_quadro_real_minhas_tarefa(self):
        self.quadro.name = "Minhas Tarefa"
        with patch.dict(os.environ, {"TRELLO_BOARD_NAME": "Minhas Tarefa"}):
            self.assertEqual(tools.listar_tarefas()["status"], "sucesso")

    def test_data_bissexto_e_data_inexistente(self):
        self.assertTrue(tools._data_para_trello("2028-02-29").startswith("2028-02-29"))
        with self.assertRaises(ValueError):
            tools._data_para_trello("2027-02-29")

    def test_descricao_muito_longa_rejeitada(self):
        r = tools.adicionar_tarefa("Teste", "x" * 5001, "2026-11-12")
        self.assertEqual(r["status"], "erro")

    def test_lista_especifica_ausente(self):
        self.quadro.listas = [Lista("A fazer", "l1")]
        self.assertEqual(tools.listar_tarefas("concluido")["status"], "erro")

    def test_fuso_invalido_sanitizado(self):
        with patch.dict(os.environ, {"APP_TIMEZONE": "Inválido/Inexistente"}):
            r = tools.get_temporal_context()
            self.assertEqual(r["status"], "erro")
            self.assertIn("Fuso", r["mensagem"])

    def test_secret_placeholder_ignorado(self):
        import sys
        from types import ModuleType
        fake = ModuleType("trello")
        calls = []
        fake.TrelloClient = lambda **kw: calls.append(kw)
        with patch.dict(sys.modules, {"trello": fake}):
            with patch.dict(os.environ, {"TRELLO_API_KEY": "key-123", "TRELLO_TOKEN": "token-123", "TRELLO_API_SECRET": "COLE_SEU_SEGREDO_TRELLO_AQUI"}):
                _CLIENTE_ORIGINAL()
        self.assertEqual(calls[0]["api_secret"], None)

    def test_ausencia_credenciais(self):
        with patch.dict(os.environ, {"TRELLO_API_KEY": "", "TRELLO_TOKEN": ""}):
            r = tools._erro(RuntimeError("Credenciais Trello ausentes. Preencha TRELLO_API_KEY e TRELLO_TOKEN no .env."))
            self.assertIn("Credenciais", r["mensagem"])


if __name__ == "__main__":
    unittest.main()

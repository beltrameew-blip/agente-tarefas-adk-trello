"""Jornada completa simulada: cria, lista, move e confirma, sem rede."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

MOD = Path(__file__).resolve().parents[1] / "adk_tarefas" / "tools.py"
spec = importlib.util.spec_from_file_location("tools_jornada_offline", MOD)
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)

class FakeCard:
    def __init__(self, nome, descricao, data, origin):
        self.id, self.name, self.desc, self.due, self.origin = "card-1", nome, descricao, data, origin
    def change_list(self, destination_id):
        dest = self.origin.board.lists_by_id[destination_id]
        self.origin.cards.remove(self)
        dest.cards.append(self)
        self.origin = dest

class FakeList:
    def __init__(self, name, id, board):
        self.name, self.id, self.board, self.cards = name, id, board, []
    def add_card(self, name, desc, due):
        card = FakeCard(name, desc, due, self)
        self.cards.append(card)
        return card
    def list_cards(self):
        return list(self.cards)

class FakeBoard:
    def __init__(self):
        self.name, self.id = "Minhas Tarefa", "board-1"
        self.lists = [FakeList(n, str(i), self) for i,n in enumerate(("A fazer", "Em andamento", "Concluído"))]
        self.lists_by_id = {li.id:li for li in self.lists}
    def list_lists(self):
        return self.lists

class FakeClient:
    def __init__(self, board): self.board=board
    def list_boards(self): return [self.board]

class Jornada(unittest.TestCase):
    def test_completa_simulada(self):
        board = FakeBoard()
        with patch.object(tools,"_cliente", return_value=FakeClient(board)):
            with patch.dict(os.environ,{"TRELLO_BOARD_NAME":"Minhas Tarefa","TRELLO_BOARD_ID":"","APP_TIMEZONE":"America/Sao_Paulo"}):
                self.assertEqual(tools.adicionar_tarefa("Teste DIO","Gerenciar tarefa","2026-11-12")["status"],"sucesso")
                self.assertEqual(tools.listar_tarefas("A fazer")["total"],1)
                self.assertEqual(tools.mudar_status_tarefa("Teste DIO","Em andamento")["status"],"sucesso")
                self.assertEqual(tools.listar_tarefas("Em andamento")["total"],1)
                self.assertEqual(tools.listar_tarefas("A fazer")["total"],0)
                self.assertEqual(tools.mudar_status_tarefa("Teste DIO","concluído")["status"],"sucesso")
                self.assertEqual(tools.listar_tarefas("Concluído")["total"],1)
                self.assertEqual(tools.listar_tarefas("Em andamento")["total"],0)
                self.assertEqual(tools.mudar_status_tarefa("Teste DIO","feito")["acao"],"sem_alteracao")

if __name__ == "__main__": unittest.main()

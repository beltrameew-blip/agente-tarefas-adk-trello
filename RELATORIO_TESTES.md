# Relatório de validação — Agente Inteligente de Tarefas

Atualização documental: 09/11/2026.

## Evidências existentes

- Segundo a execução local registrada antes desta atualização, **22 testes offline passaram**, usando `python -m unittest discover -s tests -v`.
- O repositório contém 21 métodos de teste no arquivo `tests/test_tools.py` e 1 teste de jornada simulada em `tests/test_jornada_offline.py`.
- As verificações offline simulam Trello e **não demonstram** conexão real à API, uso de ferramentas pelo Gemini ou funcionamento do ADK Web.
- A versão anterior deste relatório dizia contraditoriamente “22 testes” e “15 aprovados”; esta inconsistência foi corrigida. Não houve nova execução dos testes nesta revisão documental.

## Checagens de integração necessárias

- Chave Gemini autorizada para `gemini-3.5-flash-lite` e com chamadas disponíveis na cota da conta.
- Acesso real ao quadro Trello **Minhas Tarefa**.
- Criar um cartão de validação com nome exclusivo em **A fazer**, consultar, mover para **Em andamento**, mover para **Concluído**, consultar o estado final.
- Iniciar `adk web` e verificar que a conversa em linguagem natural efetivamente chama as ferramentas.

**Estado verificado:** integração externa **PENDENTE**. Não há capturas reais de Gemini/ADK e Trello anexadas nesta revisão. Não caracterizar como produção validada nem como submissão aceita na DIO.

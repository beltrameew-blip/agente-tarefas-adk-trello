# Relatório de validação local

**Projeto:** Agente Inteligente de Tarefas — Google ADK + Gemini + Trello

## Verificações executadas no ambiente de preparação

- **15 testes de unidade** executados com `python -m unittest discover -s tests -v`: **15 aprovados, 0 falhas**.
- **Sintaxe de Python:** módulos compilados sem erro usando `python -m compileall`.
- **Sem serviços externos:** testes com quadros e cartões simulados, **sem uso de credenciais reais**.
- Cenários: data ISO e fuso horário, criação de cartão, filtros de listagem, alias de status com acento, movimentação entre listas, não duplicação, ambiguidade, quadro inexistente, erro sanitizado.

## Verificações que ainda dependem da pessoa responsável

- Instalar `google-adk` e `py-trello` no Windows e validar inicialização `adk web`.
- Inserir credenciais próprias em `adk_tarefas/.env`, que **não** está versionado.
- Testar chamadas reais ao Gemini e Trello e verificar criação/listagem/movimentação.
- Capturar imagens reais do ADK e do quadro para o portfólio.

**Conclusão:** código e testes offline preparados; integração ponta a ponta permanece **não verificada** até o teste com contas reais. Não interpretar este relatório como prova de funcionamento no Trello de produção.

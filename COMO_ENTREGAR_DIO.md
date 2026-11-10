# Checklist de entrega DIO — Agente de Tarefas

1. Crie o quadro **Minhas Tarefa** no [Trello](https://trello.com/) com três listas **A fazer**, **Em andamento**, **Concluído**.
2. Obtenha API Key e Token; o Secret é opcional para token direto conforme [guia DIO](https://github.com/digitalinnovationone/agent-carbon-footprint/blob/main/agents/agent04/readme.md); crie chave Google no [AI Studio](https://aistudio.google.com/app/apikey). **Não envie nenhuma credencial a terceiros nem ao GitHub**.
3. Execute `INICIAR_WINDOWS.ps1`. Na primeira execução, ele cria o `.env` local. Preencha e salve. Na segunda, executa testes e inicia o `adk web`.
4. No navegador `http://127.0.0.1:8091`, selecione `adk_tarefas` e experimente: *Quais são minhas tarefas hoje?*; *Crie uma tarefa Revisar Python, descrição Estudar funções, prazo 2026-11-12*; *Liste tarefas*; *Mova Revisar Python para Concluído*.
5. Confira o Trello e tire dois prints reais (ADK + quadro). Guarde em `evidencias/`; o ZIP não contém prints inventados.
6. Crie **um repositório público novo** no GitHub, por exemplo `agente-tarefas-adk-trello`. Extraia o ZIP e envie **os arquivos e pastas do conteúdo**, não o ZIP fechado. Não envie `.env`, pastas `.venv` nem credenciais.
7. Revise o README no GitHub, assegure que os prints não exponham informações e que os testes rodaram.
8. Cole a URL completa do novo repositório em **Entrega do Projeto** na DIO; inclua a descrição e confirme o termo. Submeta somente se executou de fato e verificou as funcionalidades.

## Texto sugerido para a descrição na DIO (usar somente após executar)

**Agente Inteligente de Tarefas | Google ADK + Gemini + Python + Trello.** Desenvolvi um agente conversacional que organiza atividades no Trello por meio de ferramentas Python para consulta de data, criação, listagem e movimentação de cartões. Como evolução do projeto-base da DIO, implementei normalização de status com acentos, tratamento de falhas, prevenção de movimentações ambíguas, configuração flexível do quadro e correção do vencimento para o fuso America/Sao_Paulo. O repositório inclui código, testes unitários offline, guia de instalação Windows, configuração segura das credenciais e evidências reais de execução. **Tecnologias:** Python, Google ADK, Gemini, py-trello e unittest.

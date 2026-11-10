# Entrega DIO — Agente Inteligente de Tarefas

**Repositório público existente:** https://github.com/beltrameew-blip/agente-tarefas-adk-trello

**Quadro Trello existente:** https://trello.com/b/1v8jSR3b/minhas-tarefa

Não crie outros repositórios, quadros ou listas. Preserve cartões reais.

## Única etapa local de autorização e integração

1. Configure no computador `adk_tarefas/.env` (copiado de `adk_tarefas/.env.exemplo`) com `GOOGLE_API_KEY`, `TRELLO_API_KEY` e `TRELLO_TOKEN` válidos. Não compartilhe chaves nem envie `.env` ao GitHub.
2. Na raiz do projeto, use o ambiente `.venv` já instalado e execute `VALIDAR_E_INICIAR_WINDOWS.ps1`. O script **não reinstala dependências e não repete a suíte offline**; realiza uma única jornada real, criando um cartão de teste exclusivo e mantendo-o em Concluído.
3. Abra http://127.0.0.1:8091, escolha `adk_tarefas` e teste os comandos de criação, listagem e movimentação em linguagem natural. Confira o cartão no quadro. Registre capturas reais **sem segredos**.
4. Envie o link do repositório existente no campo de entrega da DIO, conforme a interface disponibilizada ao seu curso, e confira a confirmação da submissão. Só ateste integração como aprovada se obteve resultados reais.

## Descrição profissional para a DIO

**Agente Inteligente de Tarefas — Google ADK, Gemini, Python e Trello**

Desenvolvi um agente conversacional para organização de tarefas que interpreta solicitações em linguagem natural e utiliza ferramentas Python integradas à API Trello. A solução permite consultar data e hora no fuso local, criar cartões, listar tarefas por etapa e movimentá-las entre A fazer, Em andamento e Concluído. Evoluí o projeto-base com validação de entradas, normalização de acentos e status, tratamento seguro de erros, proteção contra movimentações ambíguas, configuração flexível do quadro e testes automatizados offline. O repositório contém código-fonte, documentação técnica, scripts de execução Windows e roteiro de validação de serviços externos. A integração com contas reais e as evidências da interface são documentadas separadamente dos testes simulados.

**Link:** https://github.com/beltrameew-blip/agente-tarefas-adk-trello

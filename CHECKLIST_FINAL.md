# Situação da entrega DIO — 09/11/2026

**GitHub existente:** https://github.com/beltrameew-blip/agente-tarefas-adk-trello
**Trello existente:** https://trello.com/b/1v8jSR3b/minhas-tarefa
**Quadro:** `Minhas Tarefa` / listas `A fazer`, `Em andamento`, `Concluído`.

## Já verificado
- Código Python compilado com sucesso na preparação.
- 22 testes unitários/integração simulada aprovados localmente, sem rede externa e sem credenciais.
- Modelo `gemini-3.5-flash-lite` confirmado por documentação do Google (2026).
- Arquivo `.gitignore` protege `.env` de commits comuns; o ZIP não inclui credenciais reais.
- Repositório público foi criado, e a primeira versão foi publicada (verificar se nova versão foi enviada).

## Falta realizar no Windows / contas pessoais
1. Atualizar o repositório com a VERSÃO FINAL na raiz (e não em pasta extra). O repositório previamente tinha 12 arquivos na raiz e faltavam `.gitignore` e `adk_tarefas/.env.exemplo`. Este ZIP contém tudo, mas baixar um arquivo local NÃO atualiza automaticamente o GitHub.
2. No computador, configurar `adk_tarefas/.env` com chaves pessoais. NÃO enviar esse arquivo a ninguém.
3. Executar `VALIDAR_E_INICIAR_WINDOWS.ps1` **dentro da pasta do projeto com as chaves locais**. A execução instala dependências, repete testes e testa Gemini/Trello reais, **criando um cartão de teste**.
4. Abrir http://127.0.0.1:8091, escolher `adk_tarefas`, executar criação/listagem/mudança por conversa real. Conferir o cartão no Trello.
5. Salvar capturas reais e redigidas da conversa ADK e do quadro Trello. NÃO incluir chaves, tokens, IDs sensíveis ou senhas.
6. Somente com testes reais aprovados, entregar o repositório GitHub no campo de projeto da DIO.

## Limitações
Os testes feitos no ambiente do ChatGPT **não usam chaves pessoais**, então não comprovam chamadas reais ao Gemini, à API Trello ou a execução do ADK Web no Windows. Este documento não atesta uma integração em produção.

## Entrega DIO — resumo para copiar APÓS sucesso no Windows
Agente Inteligente de Tarefas com Google ADK, Gemini 3.5 Flash-Lite, Python e Trello. Implementa consulta de data, criação, listagem e movimentação de cartões por status. Evoluções: normalização de acentos, validação de datas no fuso America/Sao_Paulo, prevenção de movimentos ambíguos, erros seguros e 22 testes locais com simulação. Repositório com documentação, roteiro Windows, configuração de credenciais protegidas e validação real do fluxo Trello.

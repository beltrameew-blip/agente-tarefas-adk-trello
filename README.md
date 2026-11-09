# Agente Inteligente de Tarefas | Google ADK + Gemini + Trello

![Python](https://img.shields.io/badge/Python-3.11%2B-blue) ![Google ADK](https://img.shields.io/badge/Google-ADK-blue) ![Trello](https://img.shields.io/badge/Trello-API-0052CC) ![Status](https://img.shields.io/badge/Status-pronto%20para%20configurar-yellow)

> **Projeto de portfólio e entrega do Bootcamp DXC — IA do Zero ao Primeiro Agente (DIO).**  
> **Autora:** Dayane Beltrame | Estudante de Análise e Desenvolvimento de Sistemas; foco em IA, backend e automação.

## 1. Visão geral

O projeto implementa um agente conversacional com **Google Agent Development Kit (ADK)** e **Gemini 3.5 Flash-Lite**, conectado a um quadro **Trello** por meio de funções Python. O objetivo é transformar solicitações em linguagem natural em ações organizadas e rastreáveis sobre tarefas do dia.

**Cenário:** ao informar suas prioridades, o usuário pode criar cartões com data e descrição, consultar atividades por etapa e comunicar o andamento. Cada ação é executada por uma ferramenta Python e depende de retorno do Trello — o modelo não deve afirmar que criou algo sem confirmação.

```text
Pessoa usuária
     |
     v
ADK Web / Conversa  ---->  Gemini (interpretação e seleção de ferramentas)
                                     |
                                     v
                            Ferramentas Python
                           /     |      |     \
                          Data  Criar  Listar  Mover
                                     |
                                     v
                              py-trello / API
                                     |
                                     v
                           Quadro Trello "DIO"
                     [A fazer] [Em andamento] [Concluído]
```

## 2. Funcionalidades

| Ferramenta | Ação | Observações |
|---|---|---|
| `get_temporal_context()` | Consulta data e hora locais | Fuso configurável, padrão `America/Sao_Paulo` |
| `adicionar_tarefa(nome_da_tarefa, descricao_da_tarefa, data_vencimento)` | Cria cartão em `A fazer` | Data ISO `AAAA-MM-DD`; vencimento enviado às 12h locais |
| `listar_tarefas(status="todas")` | Lista cartões, com filtro opcional | Aceita `concluído`, `concluido`, `feito`, etc. |
| `mudar_status_tarefa(nome_da_tarefa, novo_status)` | Move entre as três listas | Rejeita nomes duplicados, prevenindo movimento incorreto |

**Limite do escopo:** o agente **não exclui** cartões nem gerencia múltiplos quadros na mesma conversa; o quadro é escolhido pela configuração. Não é uma aplicação de produção.

## 3. Melhorias em relação ao código-base DIO

| Problema identificado | Tratamento implementado |
|---|---|
| `concluído` com acento não era aceito em todos os fluxos | Normalização Unicode + aliases de status |
| Vencimento podia ser exibido no dia anterior por fuso/UTC | Converte `AAAA-MM-DD` para **12h do dia local** com offset; horário é convenção explícita |
| Cliente e busca de quadro repetidos | `_cliente` e `_quadro` compartilhados |
| Erros de rede vazavam mensagens brutas | Tratamento uniforme com resposta segura, sem expor detalhes potencialmente sensíveis |
| Operações com nomes iguais podiam escolher o primeiro cartão | Bloqueio de movimentações ambíguas |
| Listagem com filtro inválido retornava tudo | Erro claro para status desconhecido |
| Dependências incorretas `datetime` e `dotenv` no exemplo original | Dependências corrigidas (`python-dotenv` e biblioteca padrão `datetime`) |
| Ausência de validação automatizada | Testes de unidade offline com `unittest` e objetos simulados |

> A correção de vencimento considera **data civil local sem horário fornecido**. O valor 12h evita a virada acidental para a data anterior ao converter para UTC. Não representa um prazo de 12h definido pelo usuário.

## 4. Estrutura do repositório

```text
agente-tarefas-dio/
├── adk_tarefas/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   └── .env.exemplo            # NÃO é a sua chave real
├── tests/
│   └── test_tools.py
├── evidencias/
│   └── LEIA-ME.md
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── INICIAR_WINDOWS.ps1
├── COMO_ENTREGAR_DIO.md
└── README.md
```

## 5. Pré-requisitos

- Python **3.11+** (recomendado 3.12), Windows PowerShell, macOS ou Linux.
- Conta no [Trello](https://trello.com/), com quadro `DIO` e três listas: `A fazer`, `Em andamento`, `Concluído`.
- Credenciais Trello (API Key, token e, se disponível, Secret) de acordo com o [guia da DIO](https://github.com/digitalinnovationone/agent-carbon-footprint/blob/main/agents/agent04/readme.md).
- Chave Google Gemini em [Google AI Studio](https://aistudio.google.com/app/apikey). Limites gratuitos dependem das políticas do provedor.

**Modelo:** `gemini-3.5-flash-lite` (funções/ferramentas e nível gratuito sujeito a cotas e elegibilidade da API). Usamos o modelo atual porque o Google restringiu o acesso a versões 2.5 em novos projetos. Consulte as [opções de modelos](https://ai.google.dev/gemini-api/docs/models) antes de trocar.

**Segurança:** não publique chaves, tokens, segredos ou arquivos `.env`. O `.gitignore` já impede o envio comum desses arquivos; confira o histórico do Git antes de publicar. Tokens devem ter as permissões mínimas necessárias; revogue credenciais expostas.

## 6. Iniciando no Windows (PowerShell)

Na pasta extraída do projeto, execute:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .\adk_tarefas\.env.exemplo .\adk_tarefas\.env
notepad .\adk_tarefas\.env
```

Preencha as variáveis no arquivo local `adk_tarefas/.env`, salve e, ainda na **raiz do projeto**, rode:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\adk.exe web --port 8091
```

Abra `http://127.0.0.1:8091` e selecione `adk_tarefas`. Alternativamente execute `INICIAR_WINDOWS.ps1`, que automatiza o ambiente e a inicialização. O ADK Web é somente para desenvolvimento local. <https://adk.dev/get-started/python/>

**macOS/Linux:** `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`, copie o `.env` para `adk_tarefas/`, rode os testes e `adk web --port 8091` na raiz.

## 7. Cenário de teste manual com Trello real

1. Digite `Olá, organize minhas tarefas de hoje.` — o agente deve consultar a data local.
2. Digite `Crie a tarefa Revisar Python, descrição Estudar funções, vencimento 2026-11-12.` — valide se o cartão existe em **A fazer**, com descrição e data corretas.
3. Digite `Liste minhas tarefas a fazer.` — confira se o agente recupera o cartão do Trello.
4. Digite `Mova Revisar Python para Em andamento.` — verifique a mudança no quadro.
5. Digite `Concluí Revisar Python.` — confira o cartão em **Concluído**.
6. Digite `Liste tarefas concluídas.` — compare os dados da resposta com o quadro.

**Observação:** esses são **passos de teste a executar**, não evidências de execução já realizada. Os testes automatizados usam objetos simulados; só os prints reais do ADK e Trello comprovam a integração externa.

## 8. Testes automatizados

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes verificam data no fuso local, formato ISO, criação, listagem e filtros, normalização de acentos, ausência de cartões, nomes repetidos, prevenção de mudança duplicada, erros e não exposição de dados sensíveis. São **testes offline**, não fazem chamadas externas.

## 9. Evidências e resultado

Preencha a pasta [`evidencias/`](evidencias/) com capturas **reais** de uma conversa no `adk web` e do quadro Trello correspondente, depois de executar os testes manuais. O projeto não inclui screenshots simulados.

## 10. Limites e próximos passos

Esta é uma demonstração educacional e de portfólio: não implementa autorização multiusuário, filas, idempotência distribuída, deploy, logs centralizados ou confirmação humana reforçada. Para produção, esses controles precisariam de engenharia e homologação adicionais.

## 11. Fontes e créditos

- [Desafio original DIO — agent04](https://github.com/digitalinnovationone/agent-carbon-footprint/tree/main/agents/agent04) — referência de requisitos, Trello e ADK; código reestruturado e melhorias próprias.
- [Documentação oficial Google ADK (Python)](https://adk.dev/get-started/python/).
- [py-trello — biblioteca Python Trello](https://github.com/sarumont/py-trello).
- [Trello REST API](https://developer.atlassian.com/cloud/trello/rest/).

**Desenvolvimento:** Dayane Beltrame — ADS, Engenharia de IA e Automação. Projeto de aprendizagem, não associado oficialmente ao Google, Atlassian ou Microsoft.

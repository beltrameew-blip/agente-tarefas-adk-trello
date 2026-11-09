# Roteiro de conversa para demonstrar o agente no ADK Web

**Execute um comando de cada vez, aguardando a ferramenta retornar.** Não afirme sucesso sem ver a operação real no quadro. Use uma data futura válida para sua própria execução no campo vencimento.

1. `Olá! Qual é a data de hoje? Quero planejar minhas tarefas.`
2. `Crie uma tarefa chamada Revisar Python, descrição Estudar funções e APIs, vencimento 2026-11-12.`
3. `Liste todas as tarefas do quadro.`
4. `Mova a tarefa Revisar Python para Em andamento.`
5. `Concluí Revisar Python. Mova para Concluído.`
6. `Liste apenas as tarefas concluídas.`
7. `Mostre minhas tarefas a fazer.`

## Testes de validação negativa (não devem alterar cartões)

- `Mova a tarefa inexistente para Concluído.` → erro claro.
- `Liste o status talvez.` → erro de status inválido.
- Crie dois cartões homônimos manualmente no quadro e tente mover por nome → deve impedir a movimentação ambígua.
- `Exclua todos os cartões.` → agente deve informar que não possui ferramenta para exclusão.

## Resultado esperado

Cada operação de criação ou mudança de estado deve ter correspondência visível no Trello. Capture o ADK Web **e** o quadro, sem chaves ou tokens no print. O relatório de 15 testes offline **não substitui** a validação ponta a ponta.

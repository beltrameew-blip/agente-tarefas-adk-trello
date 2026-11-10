# Executa testes offline, checa conexões REAIS e inicia o ADK Web.
# Execute em sua pasta LOCAL, após configurar adk_tarefas/.env.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Test-Path '.\adk_tarefas\.env')) {
    Write-Host 'ERRO: Falta adk_tarefas/.env com suas chaves (somente no seu computador).' -ForegroundColor Red
    exit 1
}
& py -3.12 --version
if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 nao esta disponivel.' }
if (-not (Test-Path '.\.venv\Scripts\python.exe')) { & py -3.12 -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias.' }
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Testes offline reprovaram.' }
Write-Host 'TESTE REAL: consultando Gemini e Trello (gera pequena chamada à API).' -ForegroundColor Cyan
& .\.venv\Scripts\python.exe .\VALIDAR_INTEGRACAO.py --completo
if ($LASTEXITCODE -ne 0) { throw 'Teste real falhou. Nao atribuir status concluido.' }
Write-Host 'ADK Web disponivel em: http://127.0.0.1:8091' -ForegroundColor Green
& .\.venv\Scripts\adk.exe web --port 8091

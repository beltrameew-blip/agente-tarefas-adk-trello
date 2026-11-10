# Validação real única e ADK Web. Sem instalações/repetições automáticas.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$adk = Join-Path $PSScriptRoot '.venv\Scripts\adk.exe'
$envFile = Join-Path $PSScriptRoot 'adk_tarefas\.env'
if (-not (Test-Path -LiteralPath $python)) {
    throw 'Ambiente .venv ausente. Use o ambiente Python 3.12 já instalado; não foi feita instalação automática.'
}
if (-not (Test-Path -LiteralPath $adk)) {
    throw 'Executável ADK ausente neste ambiente. Verifique a instalação existente antes de instalar algo.'
}
if (-not (Test-Path -LiteralPath $envFile)) {
    Write-Host 'PENDENTE: configure as credenciais apenas em adk_tarefas\.env (use .env.exemplo como modelo).'
    exit 2
}
# Verificações de placeholders e variáveis vazias são feitas em VALIDAR_INTEGRACAO.py.
Write-Host 'Validando serviços reais uma vez: Gemini e quadro Trello existente.'
& $python (Join-Path $PSScriptRoot 'VALIDAR_INTEGRACAO.py') --completo
if ($LASTEXITCODE -ne 0) { throw 'Integração real NÃO aprovada. Verifique a configuração local sem divulgar segredos.' }
Write-Host 'Gemini e fluxo Trello validados. ADK Web em http://127.0.0.1:8091'
Write-Host 'PENDENTE: validar conversa real do agente na interface antes de entregar.'
& $adk web --port 8091
if ($LASTEXITCODE -ne 0) { throw 'ADK Web encerrou com erro.' }

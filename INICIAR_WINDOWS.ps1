$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
Write-Host '1) Verificando ambiente Python 3.12...'
py -3.12 --version
if (-not (Test-Path '.venv\Scripts\python.exe')) { py -3.12 -m venv .venv }
Write-Host '2) Instalando dependencias...'
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path '.\adk_tarefas\.env')) {
    Copy-Item '.\adk_tarefas\.env.exemplo' '.\adk_tarefas\.env'
    Write-Host 'ARQUIVO .env CRIADO. Preencha suas chaves LOCALMENTE. Nao compartilhe.'
    notepad.exe '.\adk_tarefas\.env'
    Write-Host 'Depois de salvar o .env, execute novamente este script.'
    exit 0
}
Write-Host '3) Executando testes offline...'
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Os testes falharam; nao iniciar ADK.' }
Write-Host '4) ADK Web: abra http://127.0.0.1:8091 no navegador.'
& .\.venv\Scripts\adk.exe web --port 8091

# Entrada compatível com versões anteriores. Sem instalações nem testes redundantes.
$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'VALIDAR_E_INICIAR_WINDOWS.ps1')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

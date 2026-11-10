# Execute na pasta onde o ZIP deste pacote foi extraído, com Git já autenticado.
# Publica SOMENTE documentação/configuração segura no repositório existente.
$ErrorActionPreference = 'Stop'
$repoUrl = 'https://github.com/beltrameew-blip/agente-tarefas-adk-trello.git'
$origem = $PSScriptRoot
$destino = Join-Path $env:TEMP 'dio-agente-tarefas-publicacao-segura'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git não está disponível. Execute a atualização no Work autorizado ou instale/autentique Git conscientemente.' }
if (Test-Path -LiteralPath $destino) { throw "Diretório temporário já existe: $destino. Nada foi sobrescrito." }
& git clone --quiet $repoUrl $destino
if ($LASTEXITCODE -ne 0) { throw 'Falha no clone do repositório existente.' }
Push-Location $destino
try {
    if ((& git status --porcelain).Count -gt 0) { throw 'Clone não está limpo; operação interrompida.' }
    $arquivos = @('.gitignore','adk_tarefas/.env.exemplo','VALIDAR_E_INICIAR_WINDOWS.ps1','INICIAR_WINDOWS.ps1','RELATORIO_TESTES.md','COMO_ENTREGAR_DIO.md','FINALIZAR_DIO_WINDOWS.ps1')
    foreach ($arquivo in $arquivos) {
        $source = Join-Path $origem ($arquivo.Replace('/',[IO.Path]::DirectorySeparatorChar))
        $target = Join-Path $destino ($arquivo.Replace('/',[IO.Path]::DirectorySeparatorChar))
        if (-not (Test-Path -LiteralPath $source)) { throw "Arquivo necessário não encontrado: $arquivo" }
        $parent = Split-Path -Parent $target
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        Copy-Item -LiteralPath $source -Destination $target -Force
    }
    # Atualizar o README sem sobrescrever sua documentação técnica existente.
    $readmePath = Join-Path $destino 'README.md'
    $marcador = '## Atualização de entrega e validação — 09/11/2026'
    $atual = Get-Content -LiteralPath $readmePath -Raw -Encoding UTF8
    if (-not $atual.Contains($marcador)) {
        $apendice = Get-Content -LiteralPath (Join-Path $origem 'NOTAS_FINAIS_README.md') -Raw -Encoding UTF8
        [IO.File]::AppendAllText($readmePath, $apendice, [Text.UTF8Encoding]::new($false))
    }
    $antiga = 'agente-tarefas-dio-pronto-para-github'
    if (Test-Path -LiteralPath $antiga) {
        $arquivosAntigos = Get-ChildItem -LiteralPath $antiga -Recurse -File
        foreach ($item in $arquivosAntigos) {
            $relativo = $item.FullName.Substring((Resolve-Path $antiga).Path.Length + 1)
            if (-not (Test-Path -LiteralPath (Join-Path $destino $relativo))) {
                throw "Remoção cancelada: conteúdo antigo sem correspondente na raiz: $relativo"
            }
        }
        & git rm -qr -- $antiga
        if ($LASTEXITCODE -ne 0) { throw 'Não foi possível preparar a remoção segura da pasta duplicada.' }
    }
    & git add -- README.md .gitignore adk_tarefas/.env.exemplo VALIDAR_E_INICIAR_WINDOWS.ps1 INICIAR_WINDOWS.ps1 RELATORIO_TESTES.md COMO_ENTREGAR_DIO.md FINALIZAR_DIO_WINDOWS.ps1
    if ($LASTEXITCODE -ne 0) { throw 'Git add falhou.' }
    # Defesa em profundidade: impedir inclusão acidental de qualquer .env real.
    $staged = @(& git diff --cached --name-only)
    if (@($staged | Where-Object { $_ -match '(^|/)\.env$|(^|/)\.env\.(?!exemplo$|example$)' }).Count -gt 0) {
        throw 'Bloqueio de segurança: há arquivo de credenciais no staging.'
    }
    & git diff --cached --check
    if ($LASTEXITCODE -ne 0) { throw 'Problema de whitespace no patch.' }
    if (@($staged).Count -eq 0) { Write-Host 'O repositório já possui as alterações. Nenhum commit necessário.'; return }
    & git commit -m 'chore(dio): finalizar configuracao segura, relatorio e entrega'
    if ($LASTEXITCODE -ne 0) { throw 'Git commit falhou: configure sua identidade Git local se necessário.' }
    & git push origin HEAD:main
    if ($LASTEXITCODE -ne 0) { throw "Publicação bloqueada. Commit local preservado em $destino. Autentique Git/GitHub e execute push somente após revisar." }
    Write-Host 'PUBLICAÇÃO OK: https://github.com/beltrameew-blip/agente-tarefas-adk-trello'
} finally { Pop-Location }

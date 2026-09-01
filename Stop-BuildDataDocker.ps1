$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectDir

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Nie znaleziono komendy 'docker'."
}

docker compose down

Write-Host "BuildData AI zostal zatrzymany."

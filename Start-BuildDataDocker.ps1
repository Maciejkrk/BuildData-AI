$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectDir

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Nie znaleziono komendy 'docker'. Zainstaluj i uruchom Docker Desktop, a potem uruchom ten skrypt ponownie."
}

New-Item -ItemType Directory -Force -Path (Join-Path $projectDir "outputs") | Out-Null

docker compose up --build -d

Write-Host ""
Write-Host "BuildData AI dziala lokalnie:"
Write-Host "  http://localhost:8020"
Write-Host ""
Write-Host "Status kontenera:"
docker compose ps

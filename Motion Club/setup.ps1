# =====================================================================
# Motion Club — setup local (Windows / PowerShell)
# Cria a venv, instala dependências, migra, popula o banco e sobe o site.
# Uso:  powershell -ExecutionPolicy RemoteSigned -File setup.ps1
# =====================================================================
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# 1. Encontrar o Python
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) {
  Write-Host "Python nao encontrado. Instale em https://www.python.org/downloads/ (marque 'Add python.exe to PATH')." -ForegroundColor Red
  exit 1
}
Write-Host "Usando Python: $($py.Source)" -ForegroundColor Cyan

# 2. Ambiente virtual
if (-not (Test-Path ".venv")) {
  Write-Host "Criando ambiente virtual (.venv)..."
  & $py.Source -m venv .venv
}
$pyExe = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

# 3. Dependencias
& $pyExe -m pip install --upgrade pip
& $pyExe -m pip install -r requirements.txt

# 4. Banco de dados + dados de exemplo
& $pyExe manage.py makemigrations core
& $pyExe manage.py migrate
& $pyExe manage.py seed

# 5. Servidor
Write-Host "`nPronto! Abrindo http://127.0.0.1:8000/" -ForegroundColor Green
& $pyExe manage.py runserver

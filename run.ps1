$ErrorActionPreference = 'Stop'

$projectRoot = $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
$mainPath = Join-Path $projectRoot 'main.py'

if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
	$pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue

	if ($null -eq $pythonCommand) {
		throw 'Python was not found. Install Python or create the virtual environment in .venv.'
	}

	$pythonPath = $pythonCommand.Source
}

Set-Location -LiteralPath $projectRoot
& $pythonPath $mainPath
exit $LASTEXITCODE
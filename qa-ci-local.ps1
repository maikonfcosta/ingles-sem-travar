$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    python checks/validate.py
    if ($LASTEXITCODE -ne 0) { throw 'Browser validation failed.' }
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'Whitespace validation failed.' }
    Write-Output 'qa-ci-local passed.'
} finally {
    Pop-Location
}

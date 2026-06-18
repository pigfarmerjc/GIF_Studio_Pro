[CmdletBinding()]
param(
    [string]$PythonPath = $env:PYTHON_PATH,
    [string]$CertificateThumbprint = $env:CODE_SIGNING_CERT_THUMBPRINT,
    [string]$TimestampUrl = "http://timestamp.digicert.com"
)

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
$outputFile = Join-Path $projectRoot "dist\GIF_Studio_Pro.exe"

if (-not $PythonPath) {
    $pythonCandidates = @(
        Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe" -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending |
            Select-Object -ExpandProperty FullName
    )
    $PythonPath = $pythonCandidates | Select-Object -First 1
}
if (-not $PythonPath -or -not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw "Python was not found. Pass -PythonPath or set the PYTHON_PATH environment variable."
}

Push-Location $projectRoot
try {
    & $PythonPath -m PyInstaller --clean --noconfirm "GIF_Studio_Pro.spec"
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed with exit code $LASTEXITCODE."
    }

    if (-not $CertificateThumbprint) {
        Write-Warning "The executable is unsigned. Smart App Control may block it; sign release builds with a trusted code-signing certificate."
        return
    }

    $signTool = Get-Command signtool.exe -ErrorAction SilentlyContinue
    if (-not $signTool) {
        throw "signtool.exe was not found. Install the Windows SDK and add SignTool to PATH."
    }

    & $signTool.Source sign /sha1 $CertificateThumbprint /fd SHA256 /tr $TimestampUrl /td SHA256 $outputFile
    if ($LASTEXITCODE -ne 0) {
        throw "Code signing failed with exit code $LASTEXITCODE."
    }

    & $signTool.Source verify /pa /v $outputFile
    if ($LASTEXITCODE -ne 0) {
        throw "Signature verification failed with exit code $LASTEXITCODE."
    }
} finally {
    Pop-Location
}

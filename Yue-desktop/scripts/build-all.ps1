# 一键构建：Python 后端 exe -> Tauri sidecar -> 打包桌面应用
# 用法（在 Yue-desktop 目录）：powershell -ExecutionPolicy Bypass -File scripts/build-all.ps1
# 只想要后端 exe：加 -BackendOnly
param(
    [switch]$BackendOnly
)

$ErrorActionPreference = "Stop"

$desktopDir = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path (Split-Path -Parent $desktopDir) "Yue agent"
$pythonExe  = Join-Path $backendDir ".venv\Scripts\python.exe"
$binDir     = Join-Path $desktopDir "src-tauri\binaries"

function Step($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Fail($msg) { Write-Host "ERROR: $msg" -ForegroundColor Red; exit 1 }

if (-not (Test-Path $pythonExe)) { Fail "找不到 Python 虚拟环境：$pythonExe" }
if (-not (Test-Path (Join-Path $backendDir "main.py"))) { Fail "找不到后端 main.py：$backendDir" }

# ── 1. 打包 Python 后端为单文件 exe ──
Step "打包 Python 后端（PyInstaller）"
Push-Location $backendDir
try {
    & $pythonExe -m PyInstaller build_sidecar.spec --noconfirm --clean
    if ($LASTEXITCODE -ne 0) { Fail "PyInstaller 构建失败" }
} finally {
    Pop-Location
}

$exePath = Join-Path $backendDir "dist\yue-backend.exe"
if (-not (Test-Path $exePath)) { Fail "未生成 $exePath" }
Write-Host "后端 exe: $exePath" -ForegroundColor Green

# ── 2. 复制到 src-tauri/binaries，按 Tauri 规则加 target triple 后缀 ──
Step "安装为 Tauri sidecar"
$rustTarget = (& rustc -vV | Select-String '^host:').ToString().Replace("host:", "").Trim()
if (-not $rustTarget) { Fail "无法获取 Rust target triple" }
Write-Host "target triple: $rustTarget"

New-Item -ItemType Directory -Force -Path $binDir | Out-Null
$sidecarName = "yue-backend-$rustTarget.exe"
Copy-Item $exePath (Join-Path $binDir $sidecarName) -Force
Write-Host "sidecar: $binDir\$sidecarName" -ForegroundColor Green

# ── 3. 准备后端运行时资源（.env + 数据目录）──
Step "准备运行时资源"
$backendDist = Join-Path $desktopDir "backend-dist"
New-Item -ItemType Directory -Force -Path $backendDist | Out-Null
$envSrc = Join-Path $backendDir ".env"
if (Test-Path $envSrc) {
    Copy-Item $envSrc (Join-Path $backendDist ".env") -Force
    Write-Host "已复制 .env（安装后会落在程序目录，可自行修改）" -ForegroundColor Green
} else {
    Write-Host "WARN: 后端没有 .env，运行时会因缺少 AUTH_TOKEN/ADMIN_PASSWORD 启动失败" -ForegroundColor Yellow
}

if ($BackendOnly) {
    Write-Host "`n[BackendOnly] 完成，未打包桌面应用。" -ForegroundColor Green
    exit 0
}

# ── 4. 打包 Tauri 桌面应用 ──
Step "打包 Tauri 桌面应用"
Push-Location $desktopDir
try {
    & npm run tauri build
    if ($LASTEXITCODE -ne 0) { Fail "Tauri 打包失败" }
} finally {
    Pop-Location
}

Step "完成"
Write-Host "安装包在: $desktopDir\src-tauri\target\release\bundle" -ForegroundColor Green

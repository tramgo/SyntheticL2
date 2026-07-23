param(
    [string[]]$Dates = @("2026-07-10", "2026-07-14"),
    [string]$ShareSasToken = $env:AZURE_STORAGE_SAS_TOKEN,
    [string]$StorageAccount = "stctrade1ramic",
    [string]$ShareName = "ctrade1-l2-data",
    [string]$RemoteRoot = "raw_l2",
    [string]$DestinationRoot = "scratch_azcopy_selected\raw_l2",
    [string]$AzCopyPath = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Resolve-AzCopy {
    param([string]$ExplicitPath)
    if ($ExplicitPath -and (Test-Path -LiteralPath $ExplicitPath)) {
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $fromPath = Get-Command azcopy.exe -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source
    if ($fromPath) {
        return $fromPath
    }
    $fromTemp = Get-ChildItem $env:TEMP -Recurse -Filter azcopy.exe -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1 -ExpandProperty FullName
    if ($fromTemp) {
        return $fromTemp
    }
    throw "azcopy.exe was not found. Install AzCopy v10 or pass -AzCopyPath."
}

function Protect-Url {
    param([string]$Url)
    return ($Url -replace 'sig=[^&\s]+', 'sig=REDACTED')
}

function Get-ParquetSummary {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        return [pscustomobject]@{ Count = 0; Bytes = 0 }
    }
    $summary = Get-ChildItem -LiteralPath $Path -Recurse -File -Filter *.parquet -ErrorAction SilentlyContinue |
        Measure-Object -Property Length -Sum
    $bytes = 0
    if ($null -ne $summary.Sum) {
        $bytes = [int64]$summary.Sum
    }
    return [pscustomobject]@{ Count = [int]$summary.Count; Bytes = $bytes }
}

if ([string]::IsNullOrWhiteSpace($ShareSasToken)) {
    throw "Share SAS token is required. Pass -ShareSasToken or set AZURE_STORAGE_SAS_TOKEN. Required permissions: read + list on share $ShareName."
}

$sas = $ShareSasToken.Trim()
if ($sas.StartsWith("?")) {
    $sas = $sas.Substring(1)
}

$azcopy = Resolve-AzCopy -ExplicitPath $AzCopyPath
$rows = New-Object System.Collections.Generic.List[object]

foreach ($date in $Dates) {
    $source = "https://$StorageAccount.file.core.windows.net/$ShareName/$RemoteRoot/trade_date=$date`?$sas"
    $destination = $DestinationRoot
    $dateDestination = Join-Path $DestinationRoot "trade_date=$date"
    New-Item -ItemType Directory -Force -Path $destination | Out-Null

    $before = Get-ParquetSummary -Path $dateDestination
    $status = "not_started"
    $exitCode = 0
    $started = Get-Date
    if ($DryRun) {
        $status = "dry_run"
        Write-Host "[DRY-RUN] azcopy copy $(Protect-Url $source) $destination --recursive=true --from-to=FileLocal --check-md5=NoCheck --overwrite=ifSourceNewer --log-level=ERROR"
    } else {
        Write-Host "[AZCOPY] trade_date=$date -> $dateDestination"
        & $azcopy copy $source $destination --recursive=true --from-to=FileLocal --check-md5=NoCheck --overwrite=ifSourceNewer --log-level=ERROR
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 0) {
            $status = "completed"
        } else {
            $status = "failed"
        }
    }
    $ended = Get-Date
    $after = Get-ParquetSummary -Path $dateDestination
    $rows.Add([pscustomobject]@{
        trade_date = $date
        status = $status
        exit_code = $exitCode
        destination = $dateDestination
        parquet_files_before = $before.Count
        bytes_before = $before.Bytes
        parquet_files_after = $after.Count
        bytes_after = $after.Bytes
        elapsed_seconds = [math]::Round(($ended - $started).TotalSeconds, 3)
    })
    if ($exitCode -ne 0) {
        break
    }
}

$rows | Format-Table -AutoSize

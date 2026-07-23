param(
    [string[]]$Dates = @("2026-07-10", "2026-07-14"),
    [string]$ShareSasToken = $env:AZURE_STORAGE_SAS_TOKEN,
    [string]$AccountKey = $env:AZURE_STORAGE_KEY,
    [string]$StorageAccount = "stctrade1ramic",
    [string]$ShareName = "ctrade1-l2-data",
    [string]$RemoteRoot = "raw_l2",
    [string]$DestinationRoot = "scratch_azcopy_selected\raw_l2",
    [string]$AzCopyPath = "",
    [int]$SasExpiryHours = 24,
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

function Normalize-Dates {
    param([string[]]$InputDates)
    $normalized = New-Object System.Collections.Generic.List[string]
    foreach ($item in $InputDates) {
        if ([string]::IsNullOrWhiteSpace($item)) {
            continue
        }
        foreach ($part in $item.Split(",")) {
            $date = $part.Trim()
            if (-not [string]::IsNullOrWhiteSpace($date)) {
                $normalized.Add($date)
            }
        }
    }
    if ($normalized.Count -eq 0) {
        throw "At least one trade date is required."
    }
    return $normalized.ToArray()
}

function New-ShareReadListSasToken {
    param(
        [string]$StorageAccount,
        [string]$ShareName,
        [string]$AccountKey,
        [int]$ExpiryHours
    )
    if ([string]::IsNullOrWhiteSpace($AccountKey)) {
        throw "Account key is empty."
    }
    $version = "2022-11-02"
    $permissions = "rl"
    $start = (Get-Date).ToUniversalTime().AddMinutes(-5).ToString("yyyy-MM-ddTHH:mm:ssZ")
    $expiry = (Get-Date).ToUniversalTime().AddHours($ExpiryHours).ToString("yyyy-MM-ddTHH:mm:ssZ")
    $protocol = "https"
    $resource = "s"
    $canonicalizedResource = "/file/$StorageAccount/$ShareName"
    $stringToSign = @(
        $permissions,
        $start,
        $expiry,
        $canonicalizedResource,
        "",
        "",
        $protocol,
        $version,
        $resource,
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ) -join "`n"
    $keyBytes = [Convert]::FromBase64String($AccountKey.Trim())
    $hmac = [System.Security.Cryptography.HMACSHA256]::new($keyBytes)
    $signatureBytes = $hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($stringToSign))
    $signature = [Convert]::ToBase64String($signatureBytes)
    return "sv=$version&st=$([Uri]::EscapeDataString($start))&se=$([Uri]::EscapeDataString($expiry))&spr=$protocol&sp=$permissions&sr=$resource&sig=$([Uri]::EscapeDataString($signature))"
}

if ([string]::IsNullOrWhiteSpace($ShareSasToken) -and [string]::IsNullOrWhiteSpace($AccountKey)) {
    throw "Share SAS token or account key is required. Pass -ShareSasToken, set AZURE_STORAGE_SAS_TOKEN, pass -AccountKey, or set AZURE_STORAGE_KEY. Required permissions: read + list on share $ShareName."
}

if ([string]::IsNullOrWhiteSpace($ShareSasToken)) {
    Write-Host "[AUTH] Generating short-lived read/list share SAS locally from account key; key and signature will not be persisted."
    $ShareSasToken = New-ShareReadListSasToken -StorageAccount $StorageAccount -ShareName $ShareName -AccountKey $AccountKey -ExpiryHours $SasExpiryHours
} else {
    Write-Host "[AUTH] Using provided share SAS token; signature will be redacted in dry-run output."
}

$sas = $ShareSasToken.Trim()
if ($sas.StartsWith("?")) {
    $sas = $sas.Substring(1)
}

$azcopy = Resolve-AzCopy -ExplicitPath $AzCopyPath
$rows = New-Object System.Collections.Generic.List[object]
$normalizedDates = Normalize-Dates -InputDates $Dates

foreach ($date in $normalizedDates) {
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

param(
    [string[]]$Dates = @("2026-07-10", "2026-07-14"),
    [string]$EnvPath = ".env",
    [string]$StorageAccount = "stctrade1ramic",
    [string]$ShareName = "ctrade1-l2-data",
    [string]$RemoteRoot = "raw_l2",
    [string]$ScratchRoot = "scratch_azcopy_selected\raw_l2",
    [string]$TargetRoot = "real_data_sample\l2_multiday_panel",
    [string]$OutputDir = "outputs\phase174",
    [string]$Python = "python",
    [switch]$DryRun,
    [switch]$ForceDownload
)

$ErrorActionPreference = "Stop"

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

function Import-DotEnvAzureCredentials {
    param([string]$Path)
    $loaded = New-Object System.Collections.Generic.List[string]
    if (-not (Test-Path -LiteralPath $Path)) {
        return $loaded.ToArray()
    }
    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith("#")) {
            continue
        }
        $idx = $trimmed.IndexOf("=")
        if ($idx -le 0) {
            continue
        }
        $name = $trimmed.Substring(0, $idx).Trim()
        $value = $trimmed.Substring($idx + 1).Trim()
        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }
        if ($name -in @("AZURE_STORAGE_SAS_TOKEN", "AZURE_STORAGE_KEY")) {
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
            $loaded.Add($name)
        }
    }
    return $loaded.ToArray()
}

function Get-MetricValue {
    param(
        [string]$Path,
        [string]$Metric,
        [string]$Default = ""
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        return $Default
    }
    $row = Import-Csv -LiteralPath $Path | Where-Object { $_.metric -eq $Metric } | Select-Object -First 1
    if ($null -eq $row) {
        return $Default
    }
    return [string]$row.value
}

function Add-Step {
    param(
        [System.Collections.Generic.List[object]]$Rows,
        [string]$StepId,
        [string]$Description,
        [string]$Status,
        [datetime]$Started,
        [datetime]$Ended,
        [int]$ExitCode,
        [string]$Command,
        [string]$ErrorText = ""
    )
    $Rows.Add([pscustomobject]@{
        step_id = $StepId
        description = $Description
        status = $Status
        started_utc = $Started.ToUniversalTime().ToString("o")
        ended_utc = $Ended.ToUniversalTime().ToString("o")
        elapsed_seconds = [math]::Round(($Ended - $Started).TotalSeconds, 3)
        exit_code = $ExitCode
        command = $Command
        error = $ErrorText
    })
}

function Invoke-Step {
    param(
        [System.Collections.Generic.List[object]]$Rows,
        [string]$StepId,
        [string]$Description,
        [string[]]$Command
    )
    $started = Get-Date
    $status = "completed"
    $exitCode = 0
    $errorText = ""
    try {
        & $Command[0] @($Command | Select-Object -Skip 1)
        $exitCode = $LASTEXITCODE
        if ($null -eq $exitCode) {
            $exitCode = 0
        }
        if ($exitCode -ne 0) {
            $status = "failed"
            $errorText = "External command exited with code $exitCode."
        }
    } catch {
        $status = "failed"
        $exitCode = 1
        $errorText = $_.Exception.Message
    }
    $ended = Get-Date
    Add-Step -Rows $Rows -StepId $StepId -Description $Description -Status $status -Started $started -Ended $ended -ExitCode $exitCode -Command ($Command -join " ") -ErrorText $errorText
    if ($status -eq "failed") {
        throw "$StepId failed: $errorText"
    }
}

$normalizedDates = Normalize-Dates -InputDates $Dates
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$steps = New-Object System.Collections.Generic.List[object]
$loadedCredentialNames = @(Import-DotEnvAzureCredentials -Path $EnvPath)
$sasPresent = -not [string]::IsNullOrWhiteSpace($env:AZURE_STORAGE_SAS_TOKEN)
$keyPresent = -not [string]::IsNullOrWhiteSpace($env:AZURE_STORAGE_KEY)
$credentialAvailable = $sasPresent -or $keyPresent
$downloadRan = $false
$phase172Ran = $false

$now = Get-Date
Add-Step -Rows $steps -StepId "P174_LOAD_ENV" -Description "Load Azure download credentials from .env into process environment if present; do not print or persist secret values." -Status "completed" -Started $now -Ended (Get-Date) -ExitCode 0 -Command "Import-DotEnvAzureCredentials $EnvPath" -ErrorText ""

$phase173Command = @(
    $Python,
    "scripts\run_phase173_real_l2_download_credential_preflight.py",
    "--dates"
) + $normalizedDates + @(
    "--storage-account",
    $StorageAccount,
    "--share-name",
    $ShareName,
    "--azure-cli-probe-status",
    "not_reprobed_by_phase174",
    "--azure-cli-probe-evidence",
    "phase174_uses_env_credential_path_first_to_avoid_secret_leakage"
)
Invoke-Step -Rows $steps -StepId "P174_PHASE173_PREFLIGHT" -Description "Refresh no-secret credential/download preflight after loading .env." -Command $phase173Command

if ($credentialAvailable -or $ForceDownload) {
    $downloadRan = $true
    $phase148Command = @(
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        "scripts\run_phase148_real_l2_download_refresh_workflow.ps1",
        "-Dates"
    ) + $normalizedDates + @(
        "-StorageAccount",
        $StorageAccount,
        "-ShareName",
        $ShareName,
        "-RemoteRoot",
        $RemoteRoot,
        "-ScratchRoot",
        $ScratchRoot,
        "-TargetRoot",
        $TargetRoot,
        "-Python",
        $Python
    )
    if ($DryRun) {
        $phase148Command += "-DryRun"
    }
    Invoke-Step -Rows $steps -StepId "P174_PHASE148_DOWNLOAD_REFRESH" -Description "Run Phase148 with download enabled using inherited environment credentials." -Command $phase148Command

    $phase172Ran = $true
    $phase172Command = @(
        $Python,
        "scripts\run_phase172_real_l2_receive_flow_availability_audit.py"
    )
    Invoke-Step -Rows $steps -StepId "P174_PHASE172_RERUN" -Description "Rerun Phase172 after download/import refresh." -Command $phase172Command
} else {
    $skipStarted = Get-Date
    Add-Step -Rows $steps -StepId "P174_DOWNLOAD_SKIPPED_NO_CREDENTIAL" -Description "Skip Phase148 download because neither SAS nor account key is available in .env or process environment." -Status "skipped" -Started $skipStarted -Ended (Get-Date) -ExitCode 0 -Command "credential_available=0" -ErrorText ""
}

$stepsPath = Join-Path $OutputDir "phase174_secure_download_step_ledger.csv"
$summaryPath = Join-Path $OutputDir "phase174_secure_real_l2_download_orchestrator_acceptance_summary.csv"
$reportPath = Join-Path $OutputDir "phase174_secure_real_l2_download_orchestrator_report.md"
$manifestPath = Join-Path $OutputDir "phase174_secure_real_l2_download_orchestrator_manifest.json"

$steps | Export-Csv -LiteralPath $stepsPath -NoTypeInformation

$failedSteps = @($steps | Where-Object { $_.status -eq "failed" }).Count
$phase173Summary = "outputs\phase173\phase173_real_l2_download_credential_preflight_acceptance_summary.csv"
$phase172Summary = "outputs\phase172\phase172_real_l2_receive_flow_availability_acceptance_summary.csv"
$phase148Summary = "outputs\phase148\phase148_real_l2_download_refresh_workflow_acceptance_summary.csv"
$downloadReadyNow = Get-MetricValue -Path $phase173Summary -Metric "phase173_download_ready_now" -Default "0"
$additionalDatesNeeded = Get-MetricValue -Path $phase172Summary -Metric "phase172_additional_dates_needed" -Default ""
$phase172ReplayAllowed = Get-MetricValue -Path $phase172Summary -Metric "phase172_strategy_replay_allowed" -Default "0"
$phase148ReplayAllowed = Get-MetricValue -Path $phase148Summary -Metric "phase148_strategy_replay_allowed" -Default "0"
$nextAction = if ([int]$phase172ReplayAllowed -eq 1 -or [int]$phase148ReplayAllowed -eq 1) {
    "run_downstream_real_anchor_feature_schema_gate_before_any_strategy_replay"
} elseif ($credentialAvailable -or $ForceDownload) {
    "inspect_phase148_phase172_outputs_then_download_remaining_dates_if_needed"
} else {
    "add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_to_env_or_process_then_rerun_phase174"
}

$summaryRows = New-Object System.Collections.Generic.List[object]
$summaryRows.Add([pscustomobject]@{ metric = "phase174_required_dates"; value = ($normalizedDates -join ","); description = "Dates this secure orchestrator is configured to acquire" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_env_path_checked"; value = $EnvPath; description = "Environment file checked for Azure credential names" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_azure_credential_names_loaded"; value = ($loadedCredentialNames -join ","); description = "Loaded Azure credential variable names only; secret values are not recorded" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_sas_available"; value = if ($sasPresent) { "1" } else { "0" }; description = "1 means SAS is present in process environment" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_account_key_available"; value = if ($keyPresent) { "1" } else { "0" }; description = "1 means account key is present in process environment" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_download_ran"; value = if ($downloadRan) { "1" } else { "0" }; description = "1 means Phase148 was invoked with download enabled" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_phase172_reran"; value = if ($phase172Ran) { "1" } else { "0" }; description = "1 means Phase172 was rerun after download/import" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_failed_steps"; value = [string]$failedSteps; description = "Workflow steps failed" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_phase173_download_ready_now"; value = $downloadReadyNow; description = "Phase173 download readiness after .env load" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_phase172_additional_dates_needed"; value = $additionalDatesNeeded; description = "Additional complete local real L2 dates still needed" })
$summaryRows.Add([pscustomObject]@{ metric = "phase174_strategy_replay_allowed"; value = "0"; description = "Secure download orchestration does not unlock strategy replay" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_paper_or_live_acceptance_allowed"; value = "0"; description = "Paper/live remains closed" })
$summaryRows.Add([pscustomobject]@{ metric = "phase174_next_best_action"; value = $nextAction; description = "Recommended next milestone" })
$summary = $summaryRows.ToArray()
$summary | Export-Csv -LiteralPath $summaryPath -NoTypeInformation

$reportLines = New-Object System.Collections.Generic.List[string]
$reportLines.Add("# Phase174 Secure Real L2 Download Orchestrator")
$reportLines.Add("")
$reportLines.Add("Generated UTC: $((Get-Date).ToUniversalTime().ToString("o"))")
$reportLines.Add("")
$reportLines.Add("Phase174 loads Azure credential variable names from `.env` or the process environment without printing or persisting secret values.")
$reportLines.Add("If a SAS or account key is available, it runs Phase148 download/import refresh and then reruns Phase172.")
$reportLines.Add("If no credential is available, it records a no-secret skipped-download ledger.")
$reportLines.Add("")
$reportLines.Add("## Acceptance Summary")
$reportLines.Add("")
foreach ($line in ($summary | ConvertTo-Csv -NoTypeInformation)) {
    $reportLines.Add($line)
}
$reportLines.Add("")
$reportLines.Add("## Step Ledger")
$reportLines.Add("")
foreach ($line in ($steps | ConvertTo-Csv -NoTypeInformation)) {
    $reportLines.Add($line)
}
Set-Content -LiteralPath $reportPath -Value $reportLines.ToArray() -Encoding UTF8

$manifest = [ordered]@{
    generated_utc = (Get-Date).ToUniversalTime().ToString("o")
    scope = "phase174_secure_real_l2_download_orchestrator"
    dates = $normalizedDates
    env_path_checked = $EnvPath
    loaded_credential_names = $loadedCredentialNames
    secrets_recorded = "none"
    download_ran = $downloadRan
    phase172_reran = $phase172Ran
    strategy_replay_policy = "closed"
    outputs = [ordered]@{
        step_ledger = $stepsPath
        acceptance_summary = $summaryPath
        report = $reportPath
        manifest = $manifestPath
    }
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$summary | Format-Table -AutoSize

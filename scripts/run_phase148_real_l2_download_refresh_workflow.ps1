param(
    [string[]]$Dates = @("2026-07-10", "2026-07-14"),
    [string]$ShareSasToken = $env:AZURE_STORAGE_SAS_TOKEN,
    [string]$AccountKey = $env:AZURE_STORAGE_KEY,
    [string]$StorageAccount = "stctrade1ramic",
    [string]$ShareName = "ctrade1-l2-data",
    [string]$RemoteRoot = "raw_l2",
    [string]$ScratchRoot = "scratch_azcopy_selected\raw_l2",
    [string]$TargetRoot = "real_data_sample\l2_multiday_panel",
    [string]$AzCopyPath = "",
    [int]$SasExpiryHours = 24,
    [string]$OutputDir = "outputs\phase148",
    [string]$Python = "python",
    [switch]$DryRun,
    [switch]$SkipDownload,
    [switch]$ForcePhase145
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

function Run-ExternalStep {
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
$downloadRan = $false
$phase145Ran = $false

if ($SkipDownload) {
    $now = Get-Date
    Add-Step -Rows $steps -StepId "P148_DOWNLOAD_SKIPPED" -Description "Skip AzCopy download and validate current local landing zone." -Status "skipped" -Started $now -Ended $now -ExitCode 0 -Command "SkipDownload"
} else {
    $downloadRan = $true
    $downloadCommand = @(
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        "scripts\sync_azure_real_l2_dates_azcopy.ps1",
        "-Dates"
    ) + $normalizedDates + @(
        "-StorageAccount",
        $StorageAccount,
        "-ShareName",
        $ShareName,
        "-RemoteRoot",
        $RemoteRoot,
        "-DestinationRoot",
        $ScratchRoot,
        "-SasExpiryHours",
        [string]$SasExpiryHours
    )
    if (-not [string]::IsNullOrWhiteSpace($AzCopyPath)) {
        $downloadCommand += @("-AzCopyPath", $AzCopyPath)
    }
    if (-not [string]::IsNullOrWhiteSpace($ShareSasToken)) {
        $downloadCommand += @("-ShareSasToken", $ShareSasToken)
    }
    if (-not [string]::IsNullOrWhiteSpace($AccountKey)) {
        $downloadCommand += @("-AccountKey", $AccountKey)
    }
    if ($DryRun) {
        $downloadCommand += "-DryRun"
    }
    Run-ExternalStep -Rows $steps -StepId "P148_AZCOPY_DOWNLOAD" -Description "Download required real L2 date partitions with AzCopy." -Command $downloadCommand
}

$phase147Command = @(
    $Python,
    "scripts\run_phase147_azcopy_download_intake_audit.py",
    "--scratch-root",
    $ScratchRoot,
    "--target-root",
    $TargetRoot,
    "--required-dates"
) + $normalizedDates
Run-ExternalStep -Rows $steps -StepId "P148_PHASE147_INTAKE_AUDIT" -Description "Audit local AzCopy landing-zone completeness." -Command $phase147Command

$phase147Summary = "outputs\phase147\phase147_azcopy_download_intake_audit_acceptance_summary.csv"
$canRunPhase145 = [int](Get-MetricValue -Path $phase147Summary -Metric "phase147_can_run_phase145_now" -Default "0")

if (($canRunPhase145 -eq 1) -or $ForcePhase145) {
    $phase145Ran = $true
    $phase145Command = @(
        $Python,
        "scripts\run_phase145_real_l2_post_download_refresh.py",
        "--scratch-root",
        $ScratchRoot,
        "--target-root",
        $TargetRoot,
        "--required-dates"
    ) + $normalizedDates
    Run-ExternalStep -Rows $steps -StepId "P148_PHASE145_REFRESH" -Description "Run conditional import/refresh workflow after intake readiness." -Command $phase145Command
} else {
    $now = Get-Date
    Add-Step -Rows $steps -StepId "P148_PHASE145_SKIPPED" -Description "Skip Phase145 because Phase147 says no required date is ready for import." -Status "skipped" -Started $now -Ended $now -ExitCode 0 -Command "phase147_can_run_phase145_now=0"
}

$phase146Command = @(
    $Python,
    "scripts\run_phase146_real_anchor_minimum_unlock_audit.py"
)
Run-ExternalStep -Rows $steps -StepId "P148_PHASE146_UNLOCK_AUDIT" -Description "Run final real-anchor minimum unlock audit." -Command $phase146Command

$phase146Summary = "outputs\phase146\phase146_real_anchor_minimum_unlock_audit_acceptance_summary.csv"
$stepsPath = Join-Path $OutputDir "phase148_workflow_step_ledger.csv"
$summaryPath = Join-Path $OutputDir "phase148_real_l2_download_refresh_workflow_acceptance_summary.csv"
$reportPath = Join-Path $OutputDir "phase148_real_l2_download_refresh_workflow_report.md"
$manifestPath = Join-Path $OutputDir "phase148_real_l2_download_refresh_workflow_manifest.json"

$steps | Export-Csv -LiteralPath $stepsPath -NoTypeInformation

$failedSteps = @($steps | Where-Object { $_.status -eq "failed" }).Count
$phase146ReplayAllowed = Get-MetricValue -Path $phase146Summary -Metric "phase146_strategy_replay_allowed" -Default "0"
$phase146DaysNeeded = Get-MetricValue -Path $phase146Summary -Metric "phase146_days_needed_for_min" -Default ""
$nextAction = if ([int]$phase146ReplayAllowed -eq 1) {
    "run_next_replay_gate_per_plan"
} elseif ($canRunPhase145 -eq 1 -and -not $phase145Ran) {
    "run_phase145_real_l2_post_download_refresh_then_phase146"
} else {
    "download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase148"
}

$stepCountValue = [string]$steps.Count
$failedStepsValue = [string]$failedSteps
$downloadRanValue = if ($downloadRan) { "1" } else { "0" }
$canRunPhase145Value = [string]$canRunPhase145
$phase145RanValue = if ($phase145Ran) { "1" } else { "0" }
$phase146ReplayAllowedValue = [string]$phase146ReplayAllowed
$phase146DaysNeededValue = [string]$phase146DaysNeeded
$nextActionValue = [string]$nextAction

$summaryRows = New-Object System.Collections.Generic.List[object]
$summaryRows.Add([pscustomobject]@{ metric = "phase148_steps"; value = $stepCountValue; description = "Workflow steps attempted or skipped" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_failed_steps"; value = $failedStepsValue; description = "Workflow steps failed" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_download_ran"; value = $downloadRanValue; description = "1 means AzCopy helper was executed by this workflow" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_phase147_can_run_phase145_now"; value = $canRunPhase145Value; description = "Phase147 intake readiness flag" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_phase145_ran"; value = $phase145RanValue; description = "1 means Phase145 was run by this workflow" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_phase146_strategy_replay_allowed"; value = $phase146ReplayAllowedValue; description = "Phase146 final replay gate" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_phase146_days_needed_for_min"; value = $phase146DaysNeededValue; description = "Additional ready real-anchor days still needed" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_strategy_replay_allowed"; value = $phase146ReplayAllowedValue; description = "Workflow never overrides Phase146" })
$summaryRows.Add([pscustomobject]@{ metric = "phase148_next_best_action"; value = $nextActionValue; description = "Recommended next milestone" })
$summary = $summaryRows.ToArray()
$summary | Export-Csv -LiteralPath $summaryPath -NoTypeInformation

$reportLines = New-Object System.Collections.Generic.List[string]
$reportLines.Add("# Phase148 Real L2 Download Refresh Workflow")
$reportLines.Add("")
$reportLines.Add("Generated UTC: $((Get-Date).ToUniversalTime().ToString("o"))")
$reportLines.Add("")
$reportLines.Add("Phase148 is an operational wrapper for the AzCopy-first real L2 path.")
$reportLines.Add("It optionally runs the AzCopy download helper, always runs Phase147 local intake, conditionally runs Phase145 only when Phase147 says a required date is ready for import, and then runs Phase146.")
$reportLines.Add("Python remains local-only; Azure bulk I/O remains in AzCopy.")
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
    scope = "phase148_real_l2_download_refresh_workflow"
    dates = $normalizedDates
    scratch_root = $ScratchRoot
    target_root = $TargetRoot
    azure_io_policy = "azcopy_only"
    python_policy = "local_validation_and_gate_refresh_only"
    outputs = [ordered]@{
        step_ledger = $stepsPath
        acceptance_summary = $summaryPath
        report = $reportPath
        manifest = $manifestPath
    }
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$summary | Format-Table -AutoSize

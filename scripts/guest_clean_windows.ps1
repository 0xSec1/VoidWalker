#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Guest-side cleanup & spoofing script for KVM/QEMU Windows VM.
    Reduces VM detection artifacts by overwriting registry keys and cleaning traces.

.DESCRIPTION
    - Removes Hyper-V/KVM enlightenment traces
    - Renames QEMU/VirtIO disk/DVD friendly names in Enum\SCSI

.NOTES
    - Run as Administrator inside the Windows guest
    - Take VM snapshot BEFORE running!
#>


Write-Host "KVM/QEMU Guest Cleanup & Spoofing" -ForegroundColor Cyan
Write-Host "BACKUP REGISTRY / TAKE VM SNAPSHOT BEFORE RUNNING!" -ForegroundColor Red -BackgroundColor Black

$confirm = Read-Host "Continue? (Y/N)"
if ($confirm -notin 'Y','y') { exit }

# =============================================================================
# 1. SCSI disk identifiers
# =============================================================================
$scsiPaths = @(
    "HKLM:\HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 1\Target Id 0\Logical Unit Id 0",
    "HKLM:\HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 2\Target Id 0\Logical Unit Id 0"
)

foreach ($path in $scsiPaths) {
    if (Test-Path $path) {
        $id = Get-ItemProperty -Path $path -Name "Identifier" -EA SilentlyContinue
        if ($id -and $id.Identifier -match "QEMU|HARDDRIVE|VirtIO|Red Hat") {
            Write-Host "Renaming Identifier in $path → SAMSUNG MZ76E120" -ForegroundColor Green
            Set-ItemProperty -Path $path -Name "Identifier" -Value "SAMSUNG MZ76E120" -Force
        }
    }
}

# =============================================================================
# 2. Enum\SCSI – rename QEMU/VirtIO disks & DVD friendly names
# =============================================================================
$enumScsi = "HKLM:\SYSTEM\CurrentControlSet\Enum\SCSI"
if (Test-Path $enumScsi) {
    Get-ChildItem -Path $enumScsi | ForEach-Object {
        $deviceKey = $_.PSPath
        $deviceName = $_.PSChildName

        # Now check only the immediate numeric instance subkeys (4&..., 5&..., etc.)
        Get-ChildItem -Path $deviceKey | ForEach-Object {
            $instanceKey = $_.PSPath
            $instanceName = $_.PSChildName

            # Skip if not a numeric instance key (skip "Device Parameters", "Properties")
            if ($instanceName -notmatch "^\d+&") { continue }

            # Check FriendlyName directly on this instance key
            $fn = Get-ItemProperty -Path $instanceKey -Name "FriendlyName" -ErrorAction SilentlyContinue
            if ($fn -and $fn.FriendlyName -match "QEMU|VirtIO|KVM|Red Hat|Bochs") {
                $isDVD = $fn.FriendlyName -match "DVD|CD-ROM|Optical"
                $newName = if ($isDVD) { "TSSTcorp CDDVDW SH-224DB" } else { "SAMSUNG MZ76E120" }
                Write-Host "Renaming FriendlyName on $deviceName\$instanceName → $newName" -ForegroundColor Green
                Set-ItemProperty -Path $instanceKey -Name "FriendlyName" -Value $newName -Force -ErrorAction SilentlyContinue
            }
        }
    }
}
else {
    Write-Host "Enum\SCSI path not found — skipping" -ForegroundColor Yellow
}

# =============================================================================
# 3. Hyper-V / KVM enlightenment traces
# =============================================================================
$hypervPaths = @(
    "HKLM:\SOFTWARE\Microsoft\Virtual Machine\Guest\Parameters",
    "HKLM:\SYSTEM\CurrentControlSet\Services\HvHost",
    "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization"
)

foreach ($path in $hypervPaths) {
    if (Test-Path $path) {
        Write-Host "Removing Hyper-V/KVM trace: $path" -ForegroundColor Green
        Remove-Item -Path $path -Recurse -Force -EA SilentlyContinue
    }
}


Write-Host "Spoofing complete." -ForegroundColor Green
Write-Host "Reboot the guest for full effect."

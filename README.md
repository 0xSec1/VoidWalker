## VoidWalker: Automated KVM/QEMU Hardening Framework
VoidWalker is a Python-based orchestration tool designed to transform standard, detectable KVM virtual machines into "Bare Metal" decoys. By manipulating the hypervisor's hardware abstraction layer, VoidWalker bypasses advanced anti-VM evasion techniques used by malware authors.

## Key Features
* **CPUID Masking**: Automatically disables the "Hypervisor Present Bit" (Bit 31 of ECX) and spoofs CPUID leaves (0x40000000) to return hardware-accurate vendor strings.

* **Dynamic SMBIOS Spoofing**: Injects randomized but realistic system identities (Dell, ASUS, etc.) including Manufacturer, Product Name, BIOS Version, and Chassis Type.

* **Intelligent UUID Synchronization**: Ensures strict parity between the top-level Domain UUID and the SMBIOS <sysinfo> block to maintain Libvirt XML integrity and prevent definition failures.

* **Automated Lab Provisioning**: Features a one-click CLI to backup existing configurations, apply hardening patches, and redefine the VM environment in seconds.

* **Network Stealth**: Randomizes MAC addresses with OUI prefixes from legitimate hardware vendors to evade network-based environment fingerprinting.

* **Disk Spoofing**: a guest-side PowerShell script (`guest_clean_windows.ps1`)(temporary workaround) that overwrites visible disk identifiers in registry locations

## Technical Stack
* **Language**: Python 3.13+.
* **Interface**: Libvirt API (via libvirt-python).
* **Parsing Engine**: lxml and xml.etree.ElementTree for robust XML transformation.

> [!NOTE]
> Only tested on Arch

## Installation
1. Clone and Enter Project:
```bash
git clone https://github.com/0xSec1/VoidWalker.git
cd VoidWalker
```
2. Initialize Virtual Environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install Core Dependencies:
```bash
pip install -r requirements.txt
```
## Usage
The harden command automates the entire cloaking process. By default, VoidWalker is configured to use the Dell hardware profile.

Primary Command:
```bash
sudo -E python3 main.py harden win10 --profile PROFILE_NAME --random-mac
```
For Disk spoofing:
1. Copy Script to Guest VM
2. Run the script
```powershell
Set-ExecutionPolicy Bypass .\guest_clean_windows.ps1

```

## Contribution
Everyone is welcome to contribute.

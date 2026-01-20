import xml.etree.ElementTree as ET
import random

def cpu_masking(root):
    cpu = root.find("cpu")
    if cpu is not None:
        root.remove(cpu)

    cpu = ET.SubElement(root, "cpu", {"mode": "host-passthrough", "check": "none"})
    # hide hypervisor feature
    ET.SubElement(cpu, "feature", {"policy": "disable", "name": "hypervisor"})

    # Hides KVM Signature
    features = root.find("features")
    if features is None:
        features = ET.SubElement(root, "features")

    old_kvm = features.find("kvm")
    if old_kvm is not None:
        features.remove(old_kvm)

    new_kvm = ET.SubElement(features, "kvm")
    ET.SubElement(new_kvm, "hidden", {"state": "on"})

def smbios_spoof(root, identity: dict):
    os_element = root.find("os")
    if os_element is None:
        raise ValueError("<os> element missing")

    smbios = os_element.find("smbios")
    if smbios is None:
        smbios = ET.SubElement(os_element, "smbios", {"mode": "sysinfo"})
    sysinfo = root.find("sysinfo")
    if sysinfo is not None:
        root.remove(sysinfo)

    sysinfo = ET.SubElement(root, "sysinfo", {"type": "smbios"})

    bios = ET.SubElement(sysinfo, "bios")
    ET.SubElement(bios, "entry", {"name": "vendor"}).text = identity["bios_vendor"]
    ET.SubElement(bios, "entry", {"name": "version"}).text = identity["bios_version"]
    ET.SubElement(bios, "entry", {"name": "date"}).text = identity["bios_date"]

    system = ET.SubElement(sysinfo, "system")
    ET.SubElement(system, "entry", {"name": "manufacturer"}).text = identity["manufacturer"]
    ET.SubElement(system, "entry", {"name": "product"}).text = identity["product"]
    ET.SubElement(system, "entry", {"name": "serial"}).text = identity["serial"]

    root_uuid = root.find("uuid").text.strip()
    ET.SubElement(system, "entry", {"name": "uuid"}).text = root_uuid
    ET.SubElement(system, "entry", {"name": "sku"}).text = identity.get("sku", "")

def randomize_network_mac(root):
    devices = root.find("devices")
    if not devices:
        return

    for iface in devices.findall("interface"):
        mac = iface.find("mac")
        if mac is not None:
            new_mac = f"00:16:3e:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}"
            mac.set("address", new_mac)
            break

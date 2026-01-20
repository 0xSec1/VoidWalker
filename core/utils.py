import os
import subprocess
import datetime
import xml.etree.ElementTree as ET
from lxml import etree

# backup original VM xml
def backup_xml(vm_name: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"/tmp/{vm_name}_original_{timestamp}.xml"
    os.system(f"virsh dumpxml {vm_name} > {backup_path}")
    return backup_path

def parse_xml(xml_path: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return tree, root

def modify_xml(tree, vm_name: str):
    # Write modified XML
    modified_path = f"/tmp/{vm_name}_modified.xml"
    tree.write(modified_path, encoding="utf-8", xml_declaration=True)

    try:
        etree.parse(modified_path)  #validates structure
    except Exception as e:
        raise ValueError(f"Invalid XML: {e}")

    result = subprocess.run(["virsh", "define", modified_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: virsh define failed!")
        print(result.stderr)
        raise RuntimeError("Failed to redefine VM")
    else:
        print(f"VM '{vm_name}' redefined. Restart to apply changes.")

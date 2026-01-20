import click
from core.utils import backup_xml, parse_xml, modify_xml
from core.arch import cpu_masking, smbios_spoof, randomize_network_mac
from core.identity import get_identity

@click.group()
def cli():
    pass

@cli.command()
@click.argument("vm_name")
@click.option("--profile", default="dell", help="dell, hp, lenovo")
@click.option("--random-mac", is_flag=True, help="Randomize network MAC")

def harden(vm_name, profile, random_mac):
    backup_path = backup_xml(vm_name)
    print(f"Backup Created: {backup_path}")

    tree, root = parse_xml(backup_path)

    identity = get_identity(profile)
    print(f"Using identity: {identity['manufacturer']} {identity['product']} (serial: {identity['serial']})")

    cpu_masking(root)
    smbios_spoof(root, identity)

    if random_mac:
        randomize_network_mac(root)

    modify_xml(tree, vm_name)
    print("Hardning applied. Restart VM")

if __name__ == "__main__":
    cli()

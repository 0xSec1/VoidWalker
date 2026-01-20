import os
import json
import random
import uuid
import string

TEMPLATE_DIR = "templates"

def load_profile(profile_name: str) -> dict:
    path = os.path.join(TEMPLATE_DIR, f"{profile_name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Profile not found: {path}")
    with open(path) as f:
        return json.load(f)

def get_identity(profile_name: str = "dell"):
    profile = load_profile(profile_name)

    manufacturer = profile["manufacturer"]
    product = random.choice(profile["product_names"])
    bios_vendor = random.choice(profile.get("bios_vendors", [manufacturer]))
    bios_version = random.choice(profile.get("bios_versions", ["1.0.0"]))

    # Serial number
    serial = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    if random.random() > 0.3:
        serial = f"{manufacturer[:3].upper()}{serial}"

    return{
        "manufacturer": manufacturer,
        "product": product,
        "serial": serial,
        "bios_vendor": bios_vendor,
        "bios_version": bios_version,
        "bios_date": "12/03/2025",
        "sku": f"{random.randint(1000,9999)}-{random.randint(100,999)}"
    }

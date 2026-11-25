import os
import hashlib
import zipfile
import xml.etree.ElementTree as ET

SRC_DIR = "src"
REPO_DIR = "repo"

def generar():
    os.makedirs(REPO_DIR, exist_ok=True)
    addons_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'

    for addon_id in os.listdir(SRC_DIR):
        addon_path = os.path.join(SRC_DIR, addon_id)
        xml_path = os.path.join(addon_path, "addon.xml")

        if not os.path.isdir(addon_path) or not os.path.exists(xml_path):
            continue

        tree = ET.parse(xml_path)
        version = tree.getroot().attrib["version"]

        with open(xml_path, "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                if not line.strip().startswith("<?xml"):
                    addons_xml += line + "\n"

        dest_folder = os.path.join(REPO_DIR, addon_id)
        os.makedirs(dest_folder, exist_ok=True)
        zip_filename = f"{addon_id}-{version}.zip"
        zip_path = os.path.join(dest_folder, zip_filename)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for foldername, _, filenames in os.walk(addon_path):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, SRC_DIR)
                    zf.write(filepath, arcname)

        print(f"Empaquetado: {zip_filename}")

    addons_xml += "</addons>\n"

    addons_xml_path = os.path.join(REPO_DIR, "addons.xml")
    with open(addons_xml_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(addons_xml)

    md5_hash = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
    with open(addons_xml_path + ".md5", "w", encoding="utf-8", newline="\n") as f:
        f.write(md5_hash)

    print("¡Repositorio generado con éxito!")

if __name__ == "__main__":
    generar()
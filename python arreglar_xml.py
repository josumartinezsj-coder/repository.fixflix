import os

dominio = "raw." + "github" + "usercontent" + ".com"
ruta_repo = "josumartinezsj-coder/repository.fixflix/main/repo"
base_url = "https://" + dominio + "/" + ruta_repo

contenido = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.fixflix" name="Repositorio FixFlix" version="1.0.2" provider-name="josumartinezsj-coder">
    <extension point="xbmc.addon.repository" name="Repositorio FixFlix">
        <dir>
            <info compressed="false">{base_url}/addons.xml</info>
            <checksum>{base_url}/addons.xml.md5</checksum>
            <datadir zip="true">{base_url}/</datadir>
        </dir>
    </extension>
    <extension point="xbmc.addon.metadata">
        <platform>all</platform>
    </extension>
</addon>
"""

os.makedirs("src/repository.fixflix", exist_ok=True)
with open("src/repository.fixflix/addon.xml", "w", encoding="utf-8", newline="\n") as f:
    f.write(contenido)

print("¡Archivo addon.xml creado correctamente sin recortes!")

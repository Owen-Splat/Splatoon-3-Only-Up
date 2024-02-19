from zs_tools import *
import work, yaml, oead


with open("objects.yml", "r") as f:
    valid_objects = yaml.safe_load(f)

level_path = "C:\\Users\\Owen3\\Desktop\\Splatoon 3 Romfs\\Splatoon 3 v983040 (0100C2500FC20800) (UPD)\\Pack\\Scene"
level = "Msn_C_01.pack.zs"

with open(f"{level_path}\\{level}", "rb") as f:
    zs_data = SARC(f.read())

# create map
file = "Banc/CraterFirst00.bcett.byml"
banc = BYAML(zs_data.writer.files[file])
banc.info['Actors'] = work.createMap(valid_objects['Basic'])
for ai in banc.info['AiGroups']:
    ai['References'] = oead.byml.Array()
banc.info['Rails'] = oead.byml.Array()
zs_data.writer.files[file] = banc.repack()

# delete graffiti
file = "Graffiti/Msn_C_01_Cmn.byml"
banc = BYAML(zs_data.writer.files[file])
banc.info['GraffitiInfo']['GraffitiObjInfo'] = oead.byml.Array()
zs_data.writer.files[file] = banc.repack()

# final
with open(f"output\\{level}", "wb") as f:
    f.write(zs_data.repack())

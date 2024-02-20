from zs_tools import *
import work
import random

with open("data.yml", "r") as f:
    data = yaml.safe_load(f)

level_path = "C:\\Users\\Owen3\\Desktop\\Splatoon 3 Romfs\\Splatoon 3 v983040 (0100C2500FC20800) (UPD)\\Pack\\Scene"
levels = ["Msn_A01_01"]

for level in levels:
    with open(f"{level_path}\\{level}.pack.zs", "rb") as f:
        zs_data = SARC(f.read())

    # create map
    file = [str(f) for f in zs_data.reader.get_files() if f.name.startswith("Banc/")][0]
    banc = BYAML(zs_data.writer.files[file])
    banc.info['Actors'] = work.createMap(data['Basic_Objects'])
    for ai in banc.info['AiGroups']:
        ai['References'] = oead.byml.Array()
    banc.info['Rails'] = oead.byml.Array()
    zs_data.writer.files[file] = banc.repack()

    # delete graffiti
    file = [str(f) for f in zs_data.reader.get_files() if f.name.startswith("Graffiti/")][0]
    banc = BYAML(zs_data.writer.files[file])
    banc.info['GraffitiInfo']['GraffitiObjInfo'] = oead.byml.Array()
    zs_data.writer.files[file] = banc.repack()

    # randomize ink color
    file = [str(f) for f in zs_data.reader.get_files() if f.name.startswith("SceneComponent/MissionMapInfo")][0]
    banc = BYAML(zs_data.writer.files[file])
    color = random.choice(data['Colors'])
    banc.info['TeamColor'] = f"Work/Gyml/{color}.game__gfx__parameter__TeamColorDataSet.gyml"

    # randomize skysphere for alterna levels, crater graphics go trippy
    if level.startswith("Msn_A"):
        file = [str(f) for f in zs_data.reader.get_files() if f.name.endswith("RenderingMission.bgyml")][0]
        banc = BYAML(zs_data.writer.files[file])
        sky = random.choice(data['Skies'])
        banc.info['Lighting']['SkySphere']['ActorName'] = f"Work/Actor/{sky}.engine__actor__ActorParam.gyml"
        zs_data.writer.files[file] = banc.repack()
    
    # delete water if it exists
    water_files = [str(f) for f in zs_data.reader.get_files() if f.name.startswith("Gyml/Msn_BrutalismWater")]
    for file in water_files:
        del zs_data.writer.files[file]
    
    # final
    with open(f"output\\{level}.pack.zs", "wb") as f:
        f.write(zs_data.repack())

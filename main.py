from zs_tools import *
from data import *
import work
import random, os

levels = [f for f in os.listdir("output") if f.endswith(".pack.zs")]
for level in levels:
    with open(f"output/{level}", "rb") as f:
        zs_data = SARC(f.read())

    # create map
    file = [str(f) for f in zs_data.reader.get_files() if f.name.startswith("Banc/")][0]
    banc = BYAML(zs_data.writer.files[file])
    banc.info['Actors'] = work.createMap()
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
    banc.info['TeamColor'] = f"Work/Gyml/{random.choice(COLORS)}.game__gfx__parameter__TeamColorDataSet.gyml"

    # randomize skysphere for alterna levels, crater graphics go trippy
    if level.startswith("Msn_A"):
        file = [str(f) for f in zs_data.reader.get_files() if f.name.endswith("RenderingMission.bgyml")][0]
        banc = BYAML(zs_data.writer.files[file])
        banc.info['Lighting']['SkySphere']['ActorName'] = f"Work/Actor/{random.choice(SKIES)}.engine__actor__ActorParam.gyml"
        zs_data.writer.files[file] = banc.repack()
    
    # delete water if it exists
    water_files = [str(f) for f in zs_data.reader.get_files() if f.name.startswith("Gyml/Msn_BrutalismWater")]
    for file in water_files:
        del zs_data.writer.files[file]
    
    # overwrite file with new data
    with open(f"output/{level}", "wb") as f:
        f.write(zs_data.repack())

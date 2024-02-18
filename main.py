from zs_tools import *
import work, yaml


with open("objects.yml", "r") as f:
    valid_objects = yaml.safe_load(f)

level_path = "C:\\Users\\Owen3\\Desktop\\Splatoon 3 Romfs\\edits\\fun\\romfs\\Pack\\Scene"
level = "Msn_A04_07C.pack.zs"

with open(f"{level_path}\\{level}", "rb") as f:
    zs_data = SARC(f.read())

msn = "fastDraw"
banc = BYAML(zs_data.writer.files[f'Banc/{msn}.bcett.byml'])
work.createMap(banc.info['Actors'], valid_objects['Basic'])
zs_data.writer.files[f'Banc/{msn}.bcett.byml'] = banc.repack()

# final
with open(f"output\\{level}", "wb") as f:
    f.write(zs_data.repack())

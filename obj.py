import oead, random, secrets


class SplatObject:
    def __init__(self, name, ids):
        self.name = name
        self.translate = []
        self.rotation = []
        self.scale = [10.0, 10.0, 10.0]
        self.team = "Neutral"

        if name not in ("DashPanel30", "Geyser", "JumpPanel"):
            self.bakeable = True
        else:
            self.bakeable = False

        # only used for checkpoints
        self.progress = 0
        self.is_last = False

        # create unique IDs for the object
        hash = ids['Hash'][-1]
        while hash in ids['Hash']:
            hash = random.getrandbits(64)
        ids['Hash'].append(hash)
        self.hash = hash

        srt_hash = ids['SRTHash'][-1]
        while srt_hash in ids['SRTHash']:
            srt_hash = random.getrandbits(32)
        ids['SRTHash'].append(srt_hash)
        self.srt_hash = srt_hash

        instance_id = ids['InstanceID'][-1]
        while instance_id in ids['InstanceID']:
            instance_id = secrets.token_hex(16)
        ids['InstanceID'].append(instance_id)
        self.instance_id = instance_id

        # determine distance of next object from current object's dimensions
        self.nextX = 0.0
        self.nextY = 0.0
        self.nextZ = 0.0
        if name.endswith('AP'):
            dims = name.strip('AP').split('x')
            n = len(dims)
            self.nextX = float(dims[n-3][-2:]) / 10 / 1.5
            self.nextY = float(dims[n-2]) / 10 / 3.0
            self.nextZ = float(dims[n-1]) / 10 / 1.2
        elif name.endswith('Fence'):
            dims = name.strip('Fence').split('x')
            n = len(dims)
            self.nextX = float(dims[n-3][-2:]) / 10 / 2.0
            self.nextY = float(dims[n-2]) / 10 / 2.35
            self.nextZ = float(dims[n-1]) / 10 / 2.0
        elif name == "DashPanel30":
            self.nextX = -1.0
            self.nextY = -5.0
            self.nextZ = 19.5
        elif name == "Geyser":
            self.nextY = random.uniform(3.0, 15.0)
        elif name == "Lft_Obj_VendingMachine":
            self.nextX = 1.0
            self.nextY = 2.0
            self.nextZ = 1.0
        elif name == "Obj_RespawnPos":
            self.team = "Alpha"
        elif name == "JumpPanel":
            self.scale = [0.5, 0.5, 0.5]
            self.nextY = 5.0
    

    def pack(self):
        objd = {}

        if self.bakeable:
            objd['Bakeable'] = True
            objd['Gyaml'] = f"Work/Actor/{self.name}.engine__actor__ActorParam.gyml"
        else:
            objd['Gyaml'] = self.name
        
        objd['Hash'] = oead.U64(self.hash)
        objd['InstanceID'] = f"{self.instance_id[:8]}-{self.instance_id[8:12]}-{self.instance_id[12:16]}-{self.instance_id[16:20]}-{self.instance_id[20:]}"
        objd['Name'] = self.name
        objd['SRTHash'] = oead.U32(self.srt_hash)
        objd['Phive'] = {'Placement': {'ID': oead.U64(self.hash)}}
        objd['Rotate'] = oead.byml.Array([oead.F32(r) for r in self.rotation])
        if self.scale != [10.0, 10.0, 10.0]:
            objd['Scale'] = oead.byml.Array([oead.F32(s) for s in self.scale])
        objd['TeamCmp'] = {'Team': self.team}
        objd['Translate'] = oead.byml.Array([oead.F32(t) for t in self.translate])

        if self.name == "MissionCheckPoint":
            objd['spl__MissionCheckPointBancParam'] = {"Progress": oead.S32(self.progress), "IsLast": self.is_last}
        elif self.name == "Geyser":
            objd['spl__GeyserBancParam'] = {'MaxHeight': oead.F32(self.nextY)}
        
        return objd

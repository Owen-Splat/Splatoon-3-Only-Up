from obj import SplatObject
import random, oead


def createMap(actors, objects):
    ids = {
        'Hash': [],
        'SRTHash': [],
        'InstanceID': []
    }

    for act in actors:
        ids['Hash'].append(act['Hash'])
        ids['SRTHash'].append(act['SRTHash'])
        ids['InstanceID'].append(act['InstanceID'])
        trans = list(act['Translate'])
        act['Translate'] = oead.byml.Array([trans[0], trans[1], oead.F32(float(trans[2]) - 500.0)])
    
    pos = [0.0, 31.5, -584.0]
    rot = [0.0, 0.0, 0.0]

    num = 200
    for i in range(num):
        if i == num-1:
            obj_name = "Lft_MsnGoalFloor180x30x90AP"
        else:
            if not (i+1) % 50:
                obj_name = "MissionCheckPoint"
            else:
                obj_name = random.choice(objects)
        
        new_object = SplatObject(obj_name, ids)
        if not (i+1) % 50:
            new_object.progress = int((i+1) / 50)
            if new_object.progress == (round(num / 50)) - 1:
                new_object.is_last = True

        if new_object.nextX > 0.0:
            pos[0] += (new_object.nextX / 2)
            pos[1] -= new_object.nextY
            pos[2] += (new_object.nextZ / 2)
        
        if obj_name in ("Lft_Obj_VendingMachine", "Lft_MsnSlope150x60x30AP", "Lft_MsnSlope60x60x150AP", "Lft_MsnSlope90x60x150AP"):
            rot[1] = 135.0
        
        new_object.translate = pos
        new_object.rotation = rot

        if i == num-1:
            pos[2] += 7.5
            rot[1] = 67.5
            new_object.translate = pos
            new_object.rotation = rot
            actors.append(new_object.pack())
            break
        
        actors.append(new_object.pack())

        # run calcs for pos/rot of next obj
        if new_object.nextX != -1.0:
            hor = random.uniform(1.5, 2.5) + new_object.nextX
            if random.randint(0, 1) == 1:
                hor = -abs(hor)
            pos[0] += hor

        pos[1] += random.uniform(0.075, 0.185) + new_object.nextY

        if new_object.nextX != -1.0:
            hor = random.uniform(2.0, 3.0) + new_object.nextZ
            pos[2] += abs(hor)
        else:
            pos[2] += new_object.nextZ

        rot[1] = 0.0 # random.uniform(0.1, 360.0)
    
    goals = ["Obj_GoalMission", "Obj_GoalMissionAlterna"]
    goal_name = random.choice(goals)
    goal_obj = SplatObject(goal_name, ids)
    pos[2] += 5.0
    goal_obj.translate = pos
    rot[1] = 135.0
    goal_obj.rotation = rot
    actors.append(goal_obj.pack())

    gate_obj = SplatObject("Lft_MsnGoalGateNP", ids)
    gate_obj.bakeable = True
    pos[2] += 15.0
    gate_obj.translate = pos
    gate_obj.rotation = rot
    actors.append(gate_obj.pack())

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
    
    pos = [0.0, 31.5, -84.0]
    rot = [0.0, 0.0, 0.0]
    sca = [10.0, 10.0, 10.0]

    num = 200
    for i in range(num):
        if i == num-1:
            obj_name = "Lft_MsnGoalFloor180x30x90AP"
        else:
            obj_name = random.choice(objects)
        
        new_object = SplatObject(obj_name, ids)
        new_object.bakeable = True

        if new_object.nextX != 0.0:
            pos[0] += (new_object.nextX / 2)
            # pos[1] -= new_object.nextY
            pos[2] += (new_object.nextZ / 2)
        
        new_object.translate = pos
        new_object.rotation = rot
        new_object.scale = sca

        if i == num-1:
            pos[2] += 7.5
            rot[1] = 67.5
            new_object.translate = pos
            new_object.rotation = rot
            actors.append(new_object.pack())
            break
        
        actors.append(new_object.pack())

        # run calcs for pos/rot of next obj
        hor = random.uniform(1.5, 2.5) + new_object.nextX
        if random.randint(0, 1) == 1:
            hor = -abs(hor)
        pos[0] += hor

        pos[1] += random.uniform(0.05, 0.2) # + new_object.nextY

        hor = random.uniform(2.0, 3.0) + new_object.nextZ
        pos[2] += abs(hor)

        # rot[1] = random.uniform(0.1, 360.0)
    
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
    pos[2] += 20.0
    gate_obj.translate = pos
    gate_obj.rotation = rot
    actors.append(gate_obj.pack())

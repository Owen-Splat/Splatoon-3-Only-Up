from obj import SplatObject
from data import *
import random, oead


def createMap():
    ids = {
        'Hash': [],
        'SRTHash': [],
        'InstanceID': []
    }
    actors = []
    pos = [0.0, 30.0, -600.0]

    num = 200
    for i in range(num):
        if i == 0:
            obj_name = "Obj_RespawnPos"
        elif i == num-1:
            obj_name = "Lft_MsnGoalFloor180x30x90AP"
        else:
            if not (i+1) % 50:
                obj_name = "MissionCheckPoint"
            else:
                obj_name = random.choice(ALL_OBJECTS)
        
        new_object = SplatObject(obj_name, ids)
        if not (i+1) % 50:
            new_object.progress = int((i+1) / 50)
            if new_object.progress == (round(num / 50)) - 1:
                new_object.is_last = True

        if new_object.nextX > 0.0:
            pos[0] += (new_object.nextX / 2)
            pos[1] -= new_object.nextY
            pos[2] += (new_object.nextZ / 2)
        
        new_object.translate = pos

        if i == num-1:
            pos[2] += 7.5
            new_object.rotation[1] = 90.0
            new_object.translate = pos
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
    
    # add a random goal at the end
    goals = ["Obj_GoalMission", "Obj_GoalMissionAlterna",
             "SplMissionStageTreasureA", "SplMissionStageTreasureB", "SplMissionStageTreasureC"]
    goal_name = random.choice(goals)
    goal_obj = SplatObject(goal_name, ids)
    if goal_name.startswith("Spl"):
        pos[1] += 2.0
    pos[2] += 5.0
    goal_obj.translate = pos
    goal_obj.rotation[1] = 180.0
    actors.append(goal_obj.pack())

    # add a gate at the end for decoration
    gate_obj = SplatObject("Lft_MsnGoalGateNP", ids)
    gate_obj.bakeable = True
    pos[2] += 15.0
    gate_obj.translate = pos
    gate_obj.rotation[1] = 180.0
    actors.append(gate_obj.pack())

    # the last Obj_RespawnPos in the actor list is the one that spawns the player, so move first actor to last
    spawn_obj = actors.pop(0)
    actors.append(spawn_obj)

    return oead.byml.Array(actors)

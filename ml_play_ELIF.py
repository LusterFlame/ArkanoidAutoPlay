import arkanoid.communication as comm
from arkanoid.communication import SceneInfo, GameInstruction

def ml_loop():
    LastXY = (100, 100)
    comm.ml_ready()
    while True:
        scene_info = comm.get_scene_info()
        if scene_info.status == SceneInfo.STATUS_GAME_OVER or \
        scene_info.status == SceneInfo.STATUS_GAME_PASS:
            scene_info = comm.get_scene_info()
        # Get the height of the avreage of the lowest 5 brick
        # But ignore outliner
        lowestBrick = list()
        for brickPos in scene_info.bricks:
            lowestBrick.append(brickPos)
        lowestBrick.sort(reverse = True, key = getY)
        while len(lowestBrick) > 5:
            lowestBrick.pop()
        for brick in lowestBrick:
            if brick - lowestBrick[0] > 100:
                lowestBrick.remove(lowestBrick.index(brick))
        average = 0
        for brick in lowestBrick:
            average = average + brick[1]
        average = average / len(lowestBrick)


        if LastXY[1] - scene_info.ball[1] > 0:
            # Code for going up
            tickTillPlat = (400 - average) * 2 / 5
            ballXToMove = tickTillPlat * 5
            if scene_info.ball[0] - LastXY[0] > 0:
                finalXDest = scene_info.ball[0] + ballXToMove
            else:
                finalXDest = scene_info.ball[0] - ballXToMove

            if finalXDest >= 400 or finalXDest <= -200 or (finalXDest >= 0 and finalXDest <= 200):
                if scene_info.platform[0] + 20 > 105:
                    comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
                elif scene_info.platform[0] + 20 < 95:
                    comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
                else:
                    comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
            elif finalXDest < 0:
                finalXDest = finalXDest * -1
            elif finalXDest > 200:
                finalXDest = 400 - finalXDest

            if scene_info.platform[0] + 20 > finalXDest + 5:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
            elif scene_info.platform[0] + 20 < finalXDest - 5:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
            else:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
        else:
            # Code for going down
            # Calc ball poition when y = 400
            TickTillPlat = (400 - scene_info.ball[1]) / 5 
            BallXtoMove = TickTillPlat * 5
            if scene_info.ball[0] - LastXY[0] > 0:
                FinalXDest = scene_info.ball[0] + BallXtoMove
                if FinalXDest >= 200 and FinalXDest < 400:
                    FinalXDest = 400 - FinalXDest
                elif FinalXDest >= 400:
                    FinalXDest -= 400
            else:
                FinalXDest = scene_info.ball[0] - BallXtoMove
                if FinalXDest <= 0 and FinalXDest > -200:
                    FinalXDest = 0 - FinalXDest
                elif FinalXDest <= -200:
                    FinalXDest += 400
                    
            if scene_info.platform[0] + 20 > FinalXDest + 5:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
            elif scene_info.platform[0] + 20 < FinalXDest - 5:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
            else:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
        
        LastXY = scene_info.ball
            
def getY(brick):
    return brick[1]
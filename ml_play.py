import arkanoid.communication as comm
from arkanoid.communication import SceneInfo, GameInstruction    

def ml_loop():
    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    LastXY = (100, 100)
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene immediately and send the scene information again.
        #      Therefore, receive the reset scene information.
        #      You can do proper actions, when the game is over or passed.
        if scene_info.status == SceneInfo.STATUS_GAME_OVER or \
        scene_info.status == SceneInfo.STATUS_GAME_PASS:
            scene_info = comm.get_scene_info()
            
        # 3.3. Put the code here to handle the scene information
        if LastXY[1] - scene_info.ball[1] > 0:
            # Code for going up
            if scene_info.platform[0] + 20 > 100:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
            elif scene_info.platform[0] + 20 < 100:
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
                    
            if scene_info.platform[0] + 20 > FinalXDest:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
            elif scene_info.platform[0] + 20 < FinalXDest:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
            else:
                comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
        
        # 3.4. Send the instruction for this frame to the game process
        LastXY = scene_info.ball
            
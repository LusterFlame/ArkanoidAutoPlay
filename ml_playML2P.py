import pingpong.communication as comm
from pingpong.communication import (
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)
import pickle
import numpy as np

def ml_loop(side: str):

    filename = "forestTrained2P.sav"
    load_model = pickle.load(open(filename, 'rb'))
    comm.ml_ready()
    while True:
        scene_info = comm.get_scene_info()
        if scene_info.frame == 0:
            LastBallPos = scene_info.ball
    
        if scene_info.status == GameStatus.GAME_1P_WIN or \
            scene_info.status == GameStatus.GAME_2P_WIN:
            comm.ml_ready()
            continue
        Direction = (scene_info.ball[1] - LastBallPos[1]) / scene_info.ball_speed


        input_temp = np.array([scene_info.ball[0], scene_info.ball[1], scene_info.platform_2P[0], Direction])
        input = input_temp[np.newaxis, :]
        a = load_model.predict(input)
        #print(a)
        LastBallPos = scene_info.ball
        if a > 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif a < 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
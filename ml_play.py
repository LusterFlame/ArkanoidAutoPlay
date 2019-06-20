import pingpong.communication as comm
from pingpong.communication import (
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)
import math


def ml_loop(side: str):
    comm.ml_ready()
    if side == '1P': # Upper
        while True:
            scene_info = comm.get_scene_info()
            ball = scene_info.ball
            speed = scene_info.ball_speed
            if scene_info.status == GameStatus.GAME_1P_WIN or \
                scene_info.status == GameStatus.GAME_2P_WIN:
                comm.ml_ready()
                continue
            if scene_info.frame == 0:
                last_scene_info = scene_info
                continue
            ## To caculate drop point
            if ball[1] > last_scene_info.ball[1]: # ball leaving board(down)
                tickLeft = (680 - (ball[1] - 80)) / scene_info.ball_speed
                if(ball[0] - last_scene_info.ball[0] > 0): # Going right
                    XDest = ball[0] + scene_info.ball_speed * tickLeft
                else:
                    XDest = ball[0] - scene_info.ball_speed * tickLeft
            else:  # ball going toward board
                tickLeft = (ball[1] - 80) / scene_info.ball_speed
                if(ball[0] - last_scene_info.ball[0] > 0): # Going right
                    XDest = ball[0] + scene_info.ball_speed * tickLeft
                else:
                    XDest = ball[0] - scene_info.ball_speed * tickLeft
            if(math.floor(XDest / 200) % 2 == 1):
                XDest = 200 - (XDest % 200)
            else:
                XDest %= 200

            if scene_info.platform_1P[0] + 20 < XDest and abs(scene_info.platform_1P[0] + 20 - XDest) >= 13:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif scene_info.platform_1P[0] + 20 > XDest and abs(scene_info.platform_1P[0] + 20 - XDest) >= 13:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            last_scene_info = scene_info

    else: # Lower
        while True:
            scene_info = comm.get_scene_info()
            ball = scene_info.ball
            speed = scene_info.ball_speed
            if scene_info.status == GameStatus.GAME_1P_WIN or \
                scene_info.status == GameStatus.GAME_2P_WIN:
                comm.ml_ready()
                continue
            if scene_info.frame == 0:
                last_scene_info = scene_info
                continue
            ## To caculate drop point
            if ball[1] < last_scene_info.ball[1]: # ball leaving board(up)
                tickLeft = (340 + (ball[1] - 80)) / scene_info.ball_speed
                if(ball[0] - last_scene_info.ball[0] > 0): # Going right
                    XDest = ball[0] + scene_info.ball_speed * tickLeft
                else:
                    XDest = ball[0] - scene_info.ball_speed * tickLeft
            else:  # ball going toward board
                tickLeft = (420 - ball[1]) / scene_info.ball_speed
                if(ball[0] - last_scene_info.ball[0] > 0): # Going right
                    XDest = ball[0] + scene_info.ball_speed * tickLeft
                else:
                    XDest = ball[0] - scene_info.ball_speed * tickLeft
            if(math.floor(XDest / 200) % 2 == 1):
                XDest = 200 - (XDest % 200)
            else:
                XDest %= 200
            if scene_info.platform_2P[0] + 20 < XDest and abs(scene_info.platform_2P[0] + 20 - XDest) >= 13:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif scene_info.platform_2P[0] + 20 > XDest and abs(scene_info.platform_2P[0] + 20 - XDest) >= 13:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            last_scene_info = scene_info
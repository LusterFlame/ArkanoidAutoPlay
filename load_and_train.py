import pickle
from pingpong.communication import (
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

data_list = []
with open("O.pickle", "rb") as f:
    data_list += pickle.load(f)

# Saving Information
Ballposition = []
PlatformPosition_1P = []
s = []
ans = []
for j in range(0, 1):
    for i in range(0, len(data_list)):
        Ballposition.append(data_list[i].ball)
        PlatformPosition_1P.append(data_list[i].platform_1P)
        s.append(data_list[i].ball_speed)
        if data_list[i].command_1P == PlatformAction.MOVE_LEFT:
            ans.append(-1)
        elif data_list[i].command_1P == PlatformAction.MOVE_RIGHT:
            ans.append(1)
        else:
            ans.append(0)
# Calculating Instruction for Each Frame Using Platform Position
import numpy as np



PlatX = np.array(PlatformPosition_1P)[:, 0][:, np.newaxis]
PlatX_next = PlatX[1:, :]
instruct = (PlatX_next - PlatX[0:len(PlatX_next), 0][:, np.newaxis])

BallY = np.array(Ballposition)[:, 1][:, np.newaxis]
BallY_next = BallY[1:, :]
instructB = (BallY_next - BallY[0:len(BallY_next), 0][:, np.newaxis])
for i in range(0, len(BallY_next)):
    instructB[i, 0] /= s[i]



# Setting x and y
Ballarray = np.array(Ballposition[:-1])
x = np.hstack((Ballarray, PlatX[0:-1, 0][:, np.newaxis], ans[0:-1]))
y = ans[:, np.newaxis]

# Using Random Forest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error 

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.0001, random_state = 810)
forest_reg = RandomForestRegressor(random_state = 114514)
forest_reg.fit(x_train, np.ravel(y_train))
y_predict = forest_reg.predict(x_test)

# Save Model
import pickle
filename = "forestTrained1P.sav"
pickle.dump(forest_reg, open(filename, 'wb'))



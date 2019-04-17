import pickle

data_list = []
for temp in range (1, 16):
    pickleFileName = "ml_lvl" + str(temp) + ".pickle"
    with open(pickleFileName, "rb") as f:
        data_list += pickle.load(f)


# Saving Information
Frame = []
Status = []
Ballposition = []
PlatformPosition = []
Bricks = []
for j in range(0, 10):
    for i in range(0, len(data_list)):
        Frame.append(data_list[i].frame)
        Status.append(data_list[i].status)
        Ballposition.append(data_list[i].ball)
        PlatformPosition.append(data_list[i].platform)
        Bricks.append(data_list[i].bricks)

# Calculating Instruction for Each Frame Using Platform Position
import numpy as np

PlatX = np.array(PlatformPosition)[:, 0][:, np.newaxis]
PlatX_next = PlatX[1:, :]
instruct = (PlatX_next - PlatX[0:len(PlatX_next), 0][:, np.newaxis]) / 5
# Amplfing first few steps when moving long distance,
for temp in range(0, len(instruct) - 10):
    MovingAlot = True
    for temp2 in range (1, 10):
        if instruct[temp + temp2] != instruct[temp]:
            MovingAlot = False
    if MovingAlot:
        instruct[temp] *= 2

# Setting x and y
Ballarray = np.array(Ballposition[:-1])
x = np.hstack((Ballarray, PlatX[0:-1, 0][:, np.newaxis], ))
y = instruct

# Using Random Forest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error 

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 810)
forest_reg = RandomForestRegressor(random_state = 114514)
forest_reg.fit(x_train, np.ravel(y_train))
y_predict = forest_reg.predict(x_test)
MSE = mean_squared_error(y_test, y_predict)
RMSE = np.sqrt(MSE)
print(RMSE)

# Save Model
import pickle
filename = "forestTrained.sav"
pickle.dump(forest_reg, open(filename, 'wb'))



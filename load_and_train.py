import pickle

with open("ml_lvl1.pickle", "rb") as f:
    data_list = pickle.load(f)
with open("ml_lvl2.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl3.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl4.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl5.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl6.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl7.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl8.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl9.pickle", "rb") as f:
    data_list += pickle.load(f)


# Saving Information
Frame = []
Status = []
Ballposition = []
PlatformPosition = []
Bricks = []
for i in range(0, len(data_list)):
    Frame.append(data_list[i].frame)
    Status.append(data_list[i].status)
    Ballposition.append(data_list[i].ball)
    PlatformPosition.append(data_list[i].platform)
    # Bricks.append(data_list[i].bricks)

# Calculating Instruction for Each Frame Using Platform Position
import numpy as np

PlatX = np.array(PlatformPosition)[:, 0][:, np.newaxis]
PlatX_next = PlatX[1:, :]
instruct = (PlatX_next - PlatX[0:len(PlatX_next), 0][:, np.newaxis]) / 5

# Setting x and y
Ballarray = np.array(Ballposition[:-1])
x = np.hstack((Ballarray, PlatX[0:-1, 0][:, np.newaxis]))
y = instruct

# Using Random Forest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error 
"""
RMSE = 1
finalI = 0
for i in range(0, 1000):
"""
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
forest_reg = RandomForestRegressor(random_state = 701)
forest_reg.fit(x_train, np.ravel(y_train))
y_predict = forest_reg.predict(x_test)
MSE = mean_squared_error(y_test, y_predict)
RMSE = np.sqrt(MSE)
print(RMSE)
"""
    if np.sqrt(MSE) < RMSE:
        RMSE = np.sqrt(MSE)
        finalI = i
print(RMSE)
print(finalI)
"""


# Save Model
import pickle
filename = "forestTrained.sav"
pickle.dump(forest_reg, open(filename, 'wb'))

"""
# load model
l_model = pickle.load(open(filename,'rb'))
yp_l = l_model.predict(x_test)
print("acc load: %f " % accuracy_score(yp_l, y_test))
"""


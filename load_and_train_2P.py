import pickle

data_list = []
#with open("A.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("B.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("C.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("D.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("E.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("F.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("G.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("H.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("I.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("J.pickle", "rb") as f:
#    data_list += pickle.load(f)
#with open("K.pickle", "rb") as f:
#    data_list += pickle.load(f)
with open("M.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("N.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("O.pickle", "rb") as f:
    data_list += pickle.load(f)
    
# Saving Information
Ballposition = []
PlatformPosition_2P = []
s = []
for j in range(0, 150):
    for i in range(0, len(data_list)):
        Ballposition.append(data_list[i].ball)
        PlatformPosition_2P.append(data_list[i].platform_2P)
        s.append(data_list[i].ball_speed)

# Calculating Instruction for Each Frame Using Platform Position
import numpy as np



PlatX = np.array(PlatformPosition_2P)[:, 0][:, np.newaxis]
PlatX_next = PlatX[1:, :]
instruct = (PlatX_next - PlatX[0:len(PlatX_next), 0][:, np.newaxis])

BallY = np.array(Ballposition)[:, 1][:, np.newaxis]
BallY_next = BallY[1:, :]
instructB = (BallY_next - BallY[0:len(BallY_next), 0][:, np.newaxis])
for i in range(0, len(BallY_next)):
    instructB[i, 0] /= s[i]

# Setting x and y
Ballarray = np.array(Ballposition[:-1])
x = np.hstack((Ballarray, PlatX[0:-1, 0][:, np.newaxis], instructB))
y = instruct

# Using Random Forest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error 

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.001, random_state = 810)
forest_reg = RandomForestRegressor(random_state = 114514)
forest_reg.fit(x_train, np.ravel(y_train))
y_predict = forest_reg.predict(x_test)

# Save Model
import pickle
filename = "forestTrained2P.sav"
pickle.dump(forest_reg, open(filename, 'wb'))



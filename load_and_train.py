import pickle
with open("ml_lvl1.pickle", "rb") as f:
    data_list = pickle.load(f)
with open("ml_lvl2.pickle", "rb") as f:
    data_list += pickle.load(f)
with open("ml_lvl3.pickle", "rb") as f:
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
    Bricks.append(data_list[i].bricks)

# Calculating Instruction for Each Frame Using Platform Position
import numpy as np
PlatX = np.array(PlatformPosition)[:, 0][:, np.newaxis]
PlatX
PlatX_next = PlatX[1:, :]
instruct = (PlatX_next - PlatX[0:len(PlatX_next), 0][:, np.newaxis]) / 5

# Setting x and y
Ballarray = np.array(Ballposition[:-1])
x = np.hstack((Ballarray, PlatX[0:-1, 0][:, np.newaxis]))
y = instruct

# Using KNN

"""


# Save Model
import pickle
filename = "ooo_example0401.sav"
pickle.dump(ooo, open(filename, 'wb'))

# load model
l_model = pickle.load(open(filename,'rb'))
yp_l = l_model.predict(x_test)
print("acc load: %f " % accuracy_score(yp_l, y_test))


"""
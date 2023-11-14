import numpy as np

skeleton = np.load("./data/student.npy")

leg = [1,2,3,4,5,6]
for i in range(skeleton.shape[0]):
    for j in range(skeleton.shape[1]):
        if j in leg:
            skeleton[i][j][3] = 0
        else:
            skeleton[i][j][3] = 0.9

np.save("./student1.npy", skeleton)
skeleton = np.load("./student1.npy")
a = 0
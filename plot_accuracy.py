import re
import math
import numpy as np
from matplotlib import pyplot as plt

filePath_angle = "./angle_map_0605_33.txt"
filePath_test = "./test_0605_33.txt"

def read_angleMap():
    angle_map = []
    with open(filePath_angle, "r", ) as f:
        lines = f.readlines()
        lines = [line.strip().replace("'", "\"") for line in lines]
        for line in lines:
            (_, x, y) = list(map(float, re.split(r'[,:]', line)))
            angle_map.append((x, y))
    return angle_map

def read_testResult():
    testResult = []
    with open(filePath_test, "r", ) as f:
        lines = f.readlines()
        lines = [line.strip().replace("'", "\"") for line in lines]
        for line in lines:
            pred_device, true_device, x, y = list(map(float, re.split(r'[:,]', line)))
            testResult.append((int(pred_device), int(true_device), x, y))
    return testResult

def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return distance

def mapping(x, y):
    angle_map = read_angleMap()
    p = (x, y)
    dis_arr = [euclaideanDistance(point, p) for point in angle_map]
    pred_device = np.argmin(dis_arr)

    return pred_device, dis_arr

angle_map = read_angleMap()
testResult = read_testResult()

x = []
y = []
for angle in angle_map:
    x.append(angle[0])
    y.append(angle[1])

plt.figure(figsize=(10, 10))
for i in range(9):
    plt.text(y[i], x[i], "num"+str(i))

plt.plot(y, x, 'sr', markersize=10)

false_loss = []
cnt_t = 0
for i in range(len(testResult)):
    predict = testResult[i][0]
    true = testResult[i][1]
    xi = testResult[i][2]
    yi = testResult[i][3]

    if predict != true:
        print("false")
        (_, dis_arr) = mapping(xi, yi)
        print("         num  distance")
        print("predict: ", predict, dis_arr[predict])
        print("true:     ", true, dis_arr[true])
        cnt_t += 1
        false_loss.append(dis_arr[predict] - dis_arr[true])

        plt.plot(yi, xi, 'oy')
        plt.text(yi, xi, "predict:" + str(predict) + ", \n" + "true:" + str(true))
    else:
        print("true\n")
        plt.plot(yi, xi, 'ob')
        plt.text(yi, xi, "true:" + str(true))

plt.show()

print("each loss: ", false_loss)
MSE = np.square(false_loss).mean()
print("MSE: ", MSE)
print("acc: ", (len(testResult)-len(false_loss))/len(testResult))

import math

def get_expected_accurasy(speed_x):
    if speed_x >= 15625:
        return "as horrible as possible"
    acc = [0.8568, 0.8556, 0.844, 0.8, 0.54, 0.13, 0.03]
    bords = [1, 5, 25, 125, 625, 3125, 15625]
    n = acc[0]
    for i in range(len(acc)):
        acc[i] /= n
    id = 1
    while speed_x >= bords[id]:
        id += 1
    p = (speed_x - bords[id-1]) / (bords[id] - bords[id-1])
    return acc[id] * p + (1 - p) * acc[id - 1]

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
    p = (speed_x - bords[id - 1]) / (bords[id] - bords[id - 1])
    return acc[id] * p + (1 - p) * acc[id - 1]


def get_segment_intersection(sset1, sset2, systime, accurasy=0.001):
    if accurasy > (sset1[0][1] - sset1[0][0]):
        raise ValueError("accurasy outstrip the distance")
    l1 = len(sset1)
    l2 = len(sset2)
    matrix = [[0, 0], [0, 0]]
    idf = 0
    ids = 0
    m1 = 0
    m2 = 0

    i = 0
    num = 0
    while i < systime:
        num += 1

        if idf < l1:
            if i > sset1[idf][1]:
                idf += 1
                m1 = 0
            if idf < l1:
                if i < sset1[idf][0]:
                    m1 = 0
                else:
                    m1 = 1

        if ids < l2:
            if i > sset2[ids][1]:
                ids += 1
                m2 = 0
            if ids < l2:
                if i < sset2[ids][0]:
                    m2 = 0
                else:
                    m2 = 1

        matrix[m1][m2] += 1

        i += accurasy

    for j in range(2):
        matrix[j][0] /= num
        matrix[j][1] /= num

    return matrix














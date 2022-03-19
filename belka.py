n = int(input())
m = []
for i in range(n):
    b, x1, y1, x2, y2 = input().split()
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    m.append((b, x1, y1, x2, y2))
aa = []
for i in m:
    v = 0
    for j in m:
        if j[0] != i[0]:
            xmax1, xmin1, xmax2, xmin2, ymax1, ymin1, ymax2, ymin2 = \
                max(i[1], i[3]), min(i[1], i[3]), max(j[1], j[3]), min(j[1], j[3]), \
                max(i[2], i[4]), min(i[2], i[4]), max(j[2], j[4]), min(j[2], j[4])
            if xmax1 >= xmin2 and xmax2 >= xmin1 and ymax1 >= ymin2 and ymax2 >= ymin1:
                p1p3, p1p2, p1p4, p3p1, p3p4, p3p2 = (j[1] - i[1], j[2] - i[2]), (i[3] - i[1], i[4] - i[2]), \
                                                     (j[3] - i[1], j[4] - i[2]), (i[1] - j[1], i[2] - j[2]), \
                                                     (j[3] - j[1], j[4] - j[2]), (i[3] - j[1], i[4] - j[2])
                if (p1p3[0] * p1p2[1] - p1p2[0] * p1p3[1]) * (p1p4[0] * p1p2[1] - p1p4[1] * p1p2[0]) <= 0 and \
                        (p3p1[0] * p3p4[1] - p3p4[0] * p3p1[1]) * (p3p2[0] * p3p4[1] - p3p2[1] * p3p4[0]) <= 0:
                    v += 1
    aa.append((i, v))
aa.sort(key=lambda x: x[1], reverse=True)
print(*[i for i in aa[0][0][1:]])

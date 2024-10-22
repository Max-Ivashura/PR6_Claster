import csv
import math
import numpy as np
from matplotlib import pyplot as plt

count = 0

t_ru = list()
t_us = list()
t_cn = list()

c_ru = [0.104040881, 0.291061881, 0.420862048]
c_us = [0.051875325, 0.269584459, 0.453281077]
c_cn = [0.000129153, 0.139262446, 0.0000685994781358219]

gr_prev = list()
gr = list()


def open_file():
    with open('NoAnomNorm.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        for line in csv_reader:
            t_ru.append(float(line[0].replace(',', '.')))
            t_us.append(float(line[1].replace(',', '.')))
            t_cn.append(float(line[2].replace(',', '.')))


def xc_calc(row1, row2, c1, c2):
    return math.sqrt((row1 - c1) ** 2 + (row2 - c2) ** 2)


def group(xc: list):
    return xc.index(min(xc))


def c_calc(t: list, gr: list, krit: int):
    total = 0
    count = 0
    for id, item in enumerate(t):
        if gr[id] == krit:
            count += 1
            total += item
    return total / count


if __name__ == '__main__':
    open_file()
    load = True
    while load:
        xc1 = list()
        xc2 = list()
        xc3 = list()
        for r1, r2 in zip(t_ru, t_us):
            xc1.append(xc_calc(r1, r2, c_ru[0], c_us[0]))
            xc2.append(xc_calc(r1, r2, c_ru[1], c_us[1]))
            xc3.append(xc_calc(r1, r2, c_ru[2], c_us[2]))

        for x1, x2, x3 in zip(xc1, xc2, xc3):
            gr.append(group([x1, x2, x3]))

        c_ru[0] = c_calc(t_ru, gr, 0)
        c_ru[1] = c_calc(t_ru, gr, 1)
        c_ru[2] = c_calc(t_ru, gr, 2)

        c_us[0] = c_calc(t_us, gr, 0)
        c_us[1] = c_calc(t_us, gr, 1)
        c_us[2] = c_calc(t_us, gr, 2)

        if gr_prev == list():
            gr_prev = gr.copy()
            gr = list()
        else:
            if gr_prev == gr:
                load = False
                print("Сгруппировано! Итераций:", count)
                s1_x = list()
                s1_y = list()
                s2_x = list()
                s2_y = list()
                s3_x = list()
                s3_y = list()
                for id, x in enumerate(gr):
                    match (x):
                        case 0:
                            s1_x.append(t_ru[id])
                            s1_y.append(t_us[id])
                        case 1:
                            s2_x.append(t_ru[id])
                            s2_y.append(t_us[id])
                        case 2:
                            s3_x.append(t_ru[id])
                            s3_y.append(t_us[id])
                plt.plot(s1_x, s1_y, 'r.', s2_x, s2_y, 'g.', s3_x, s3_y, 'b.')
                plt.show()
            else:
                gr_prev = gr.copy()
                gr = list()
                print("Итерация:", count)
                count += 1

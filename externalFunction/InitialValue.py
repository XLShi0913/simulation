# 初值与壁面物性设置
T0 = 293  # 初始温度, K
P0 = 101  # 初始压力, kPa, 对不同罐子应该修改初始条件

meshCount = 100  # 壁面网格数
dt = 1  # 时间步长, s


def setWallProp(l1, c1, l2, c2):
    # 设置壁面的物性分布的辅助函数, 长度仅作为比例，单位保持一致即可
    # 物性分布向量 = setWallConduct(长度1，系数1，长度2，系数2)
    mid = l1 / (l1 + l2) * meshCount
    res = []
    loop = 0
    while loop < mid:
        res.append(c1)
        loop += 1
    while loop < meshCount:
        res.append(c2)
        loop += 1
    return res


wallConduct = setWallProp(3, 1, 22, 2)  # 壁面导热系数, W/(m*K)
wallCapacity = setWallProp(3, 1, 22, 2)  # 壁面比热容, J/(kg*K)
wallDensity = setWallProp(3, 1, 22, 2)  # 壁面密度, kg/m^3
wallArea = 4000  # 壁面面积, m^3
wallLen = 0.025  # 壁面厚度, m

ha = 100  # 空气对流换热系数, W/(m^2*K)
hg = 100  # 氢气对流换热系数, W/(m^2*K)

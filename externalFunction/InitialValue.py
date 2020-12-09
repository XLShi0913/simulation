# 初值与壁面物性设置
# 单位制: kg, m, K, s, mol, J, Pa, W
# 计算不同罐子时, 初值需要手动设置

def setWallProp(l1, c1, l2, c2):
    # 物性设置时请看清本函数参数意义, 然后请跳过此函数, 在后面设置
    # 目标: 设置壁面的物性分布的辅助函数, 长度仅作为比例，单位保持一致即可
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


def calculate_Pout(t):
    # 控制阀出口压力与时间的函数
    return 100 * t


meshCount = 100  # 壁面网格数
dt = 1  # 时间步长, s
residual = 1E-5  # 可接受的残差
T0 = 293  # 初始温度, K
P0 = 101000  # 初始压力, Pa
M0 = 10  # 罐内初始气体质量, kg

wallConduct = setWallProp(3, 1, 22, 2)  # 壁面导热系数, W/(m*K)
wallCapacity = setWallProp(3, 1, 22, 2)  # 壁面比热容, J/(kg*K)
wallDensity = setWallProp(3, 1, 22, 2)  # 壁面密度, kg/m^3
wallArea = 4000  # 壁面面积, m^2
wallLen = 0.025  # 壁面厚度, m
volume = 100  # 罐内体积, m^3

ha = 100  # 空气对流换热系数, W/(m^2*K)
hg = 100  # 氢气对流换热系数, W/(m^2*K)

kv = 100  # 控制阀流阻系数, 无量纲

# 未在此处设置的初值：

# 传热计算模块，由给定的上一时刻的温度 + 当前罐内温度，计算壁面温度分布 + 传入储罐的热量
import externalFunction.InitialValue

iniValue = externalFunction.InitialValue
rou = iniValue.wallDensity  # 向量
c = iniValue.wallCapacity   # 向量
area = iniValue.wallArea
dx = iniValue.wallLen / iniValue.meshCount
dt = iniValue.dt
k = iniValue.wallConduct    # 向量
ha = iniValue.ha
hg = iniValue.hg
Ta = iniValue.T0
nGrid = iniValue.meshCount


def caculateT(T, dT, Tg):
    # 输入的是上一时刻的温度/温度对x的偏导
    Tpre = T[:]
    dTpre = dT[:]  # 对上一时刻的信息进行拷贝, 下面直接在T/dt上更新即可, 不需返回
    P = T[:]
    Q = T[:]  # 只是为了新建一个给定长度的列表

    A0 = 2/dt + k[0]/rou[0]/c[0]/dx/dx + hg/rou[0]/c[0]/dx
    B0 = k[0] / rou[0] / c[0] / dx / dx
    D0 = hg / rou[0] / c[0] / dx * Tg + 2 * Tpre[0] / dt + dTpre[0]
    P[0] = B0 / A0
    Q[0] = D0 / A0
    loop = 1
    while loop < nGrid - 1:
        Ai = 2 / dt + 2 * k[loop] / rou[loop] / c[loop] / dx / dx
        Bi = k[loop] / rou[loop] / c[loop] / dx / dx
        Ci = Bi
        Di = dTpre[loop] + 2 * Tpre[loop] / dt
        P[loop] = Bi / (Ai - Ci * P[loop - 1])
        Q[loop] = (Di + Ci * Q[loop - 1]) / (Ai - Ci * P[loop - 1])
        loop += 1
    loop = nGrid - 1
    An = 2/dt + k[loop]/rou[loop]/c[loop]/dx/dx + ha/rou[loop]/c[loop]/dx
    Cn = k[loop] / rou[loop] / c[loop] / dx / dx
    Dn = dTpre[loop] + 2 * Tpre[loop] / dt + ha/rou[loop]/c[loop]/dx*Ta
    P[loop] = 0
    Q[loop] = (Dn + Cn * Q[loop - 1]) / (An - Cn * P[loop - 1])
    T[nGrid - 1] = Q[nGrid - 1]
    loop = nGrid - 2
    while loop >= 0:
        T[loop] = P[loop] * T[loop + 1] + Q[loop]
        dT[loop] = 2 * (T[loop] - Tpre[loop]) / dt - dTpre[loop]
        loop -= 1
    P.clear()
    Q.clear()
    Tpre.clear()
    dTpre.clear()


def caculateQ(Twall, Tg):
    return hg * area * (Twall - Tg)

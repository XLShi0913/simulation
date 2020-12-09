# 注气过程中高压罐的计算, 控制阀流入气体的参数取决于高压罐
# 单位制: kg, m, K, s, mol, J, Pa, W

import externalFunction.PhysicalProperty
import externalFunction.ValveModular
import externalFunction.HeatTransferModular

prop = externalFunction.PhysicalProperty
valve = externalFunction.ValveModular
heatTra = externalFunction.HeatTransferModular
iniValue = heatTra.iniValue

dt = iniValue.dt
residual = iniValue.residual
V = iniValue.volume
gama = 1.4  # 氢气的绝热指数, 近似值


def calculate_tankHP(status_pre, Twall_pre, dTwall_pre, t):
    # 目标: 输出当前时刻罐内物性/罐壁温度分布
    # statue对应标号 0-P, 1-T, 2-rou, 3-h, 4-M, 5-dP, 6-drou, 7-dh, 8-dm, 9-flag(标识迭代是否收敛)
    P_pre = status_pre[0]
    T_pre = status_pre[1]
    rou_pre = status_pre[2]
    h_pre = status_pre[3]
    M_pre = status_pre[4]
    dP_pre = status_pre[5]
    drou_pre = status_pre[6]
    dh_pre = status_pre[7]

    [dm, drou] = valve.calculate_dmdrou(t, P_pre, T_pre, rou_pre)
    rou = rou_pre + 0.5 * (drou + drou_pre) * dt
    P = P_pre * (rou/rou_pre) ** gama
    T = T_pre * (rou/rou_pre) ** (gama-1)
    M = M_pre - dm * dt
    loopCounter = 0  # 迭代次数计数
    while True:
        P0 = P
        T0 = T  # 记录进入当前迭代步之前参数, 以作为迭代结束条件
        [Twall, dTwall] = heatTra.calculate_T(Twall_pre, dTwall_pre, T)
        dQ = heatTra.calculate_Q(Twall[0], T)
        dP = 2*(P-P_pre)/dt - dP_pre
        h = (h_pre*dm + V*dP + dQ)/M + dh_pre + 2*h_pre/dt
        h /= 2/dt + dm/M
        dh = 2*(h - h_pre)/dt - dh_pre
        P = prop.searchPByDH(rou, h)
        T = prop.searchTByDH(rou, h)
        loopCounter += 1
        if (P - P0 < residual or P0 - P < residual) and (T - T0 < residual or T0 - T < residual):
            flag = True
            break  # 过程收敛而退出
        if loopCounter > 1E6:
            flag = False
            break  # 过程未收敛而退出
    status = [P, T, rou, h, M, dP, drou, dh, flag]
    return [status, Twall, dTwall]  # 返回值表示了收敛与否

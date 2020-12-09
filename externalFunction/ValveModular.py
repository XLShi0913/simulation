# 气阀相关计算, 目标: 由上一时刻状态推出通过阀的质量流量
# 假设: 当前时刻通过气阀的气体, 其物性与高压罐的上一时刻一致
# 单位制: kg, m, K, s, mol, J, Pa, W
import externalFunction.InitialValue
iniValue = externalFunction.InitialValue
kv = iniValue.kv
V = iniValue.volume


def calculate_dmdrou(t, Pin, Tin, rou):
    # 质量流量 = calculate_dm(当前时间, 上一时刻高压罐: 压力, 温度, 密度)
    Pout = iniValue.calculate_Pout(t)
    k = 2 * Pin * Pout - Pout * Pout
    dm = rou * 514 * kv * (k / rou / Tin) ** 0.5
    drou = dm / V
    return [dm, drou]

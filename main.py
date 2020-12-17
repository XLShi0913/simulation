# 单位制: kg, m, K, s, mol, J, Pa, W
# 统一约定:
# 1、尽量将子类成员方法写成将传入上一时刻参数传出当前时刻参数的形式:
#    垃圾回收依靠python虚拟机;
#    子类方法对传入参数只读不写;
#    若后续想修改, 请做到格式统一;
# 2、尽量将改变参数的地方写在InitialValue中, 其他类中进行调用而不涉及参数修改;
# 3、上一时刻变量用下标_pre标识, 储气罐壁面变量用下标wall标识;

import externalFunction.TankHP
tankHP = externalFunction.TankHP
iniValue = tankHP.iniValue
prop = tankHP.prop


def calculate_tank():
    # 先只完善高压罐的部分
    # 初值定义
    t = 0
    dt = iniValue.dt
    meshCount = iniValue.meshCount
    P0 = iniValue.P0
    T0 = iniValue.T0
    rou0 = prop.searchDBYPT(P0, T0)
    h0 = prop.searchHByPD(P0, rou0)
    M0 = iniValue.M0
    status_pre = [P0, T0, rou0, h0, M0, 0, 0, 0, 0, True]
    Twall_pre = [T0] * meshCount
    dTwall_pre = [0] * meshCount
    # 用来存储想要输出的量，还可再加
    PH_res = []  # 高压罐内每一时刻压力
    TH_res = []  # 高压罐内每一时刻温度
    PL_res = []  # 低压罐内每一时刻压力
    TL_res = []  # 低压罐内每一时刻温度
    dm_res = []  # 每一时刻质量流量
    while True:  # 需要跟低压罐配合, 求出停注条件
        t += dt
        [status, Twall, dTwall] = tankHP.calculate_tankHP(status_pre, Twall_pre, dTwall_pre, t)
        if not status[9]:
            return [PH_res, TH_res, PL_res, TL_res, dm_res, t, False]  # 说明本步计算未收敛，需要进行调试
        # 在此处添加低压罐的计算模块, 与高压罐不同的是, 低压罐的质量流量是已知的
        # 参数储存与更新
        PH_res += status[0]
        TH_res += status[1]
        dm_res += (status_pre[4] - status[4]) / dt
        status_pre = status
        Twall_pre = Twall
        dTwall_pre = dTwall
        # 在此处添加低压罐压力与控制阀出口压力关系, 并据此判断结束条件
    return [PH_res, TH_res, PL_res, TL_res, dm_res, t, True]


# 主函数: 利用python IO将结果量输出

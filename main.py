# 单位制: kg, m, K, s, mol, J, Pa, W
# 统一约定:
# 1、尽量将子类成员方法写成将传入上一时刻参数传出当前时刻参数的形式:
#    垃圾回收依靠python虚拟机;
#    子类方法对传入参数只读不写;
#    若后续想修改, 请做到格式统一;
# 2、尽量将改变参数的地方写在InitialValue中, 其他类中进行调用而不涉及参数修改;
# 3、上一时刻变量用下标_pre标识, 储气罐壁面变量用下标wall标识;


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

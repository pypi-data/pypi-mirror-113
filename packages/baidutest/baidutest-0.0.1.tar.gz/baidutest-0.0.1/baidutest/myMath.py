# 定义一个类，实现加减乘除算法,对类里的加减乘除进行单元测试
class myMath():
    def add(self, a, b):
        return a + b

    def jian(self, a, b):
        return a - b

    def cheng(self, a, b):
        return a * b

    def chu(self, a, b):
        return a / b


if __name__ == "__main__":
    mm = myMath()
    mm_add = mm.add(2, 3)
    expectValue = 5
    if mm_add == expectValue:
        print("该加法功能实现正确")

    try:
        actualValue = mm.add("a", 3)
    except Exception as e:
        print("该方法实现错误", e)

    try:
        actualValue = mm.add("a", "b")
        expectValue = "ab"
        if actualValue == expectValue:
            print("该方法实现正确")
    except Exception as e:
        print("该方法实现错误", e)

# 引入框架unittest

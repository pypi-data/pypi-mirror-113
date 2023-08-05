"""
    使用unittest单元测试框架来设计mymath的单元测试用例
    步骤：
        1.导包，自带的框架，不需要安装
        2.创建一个单元测试类
        3.5个特殊方法的使用
            setUp()：主要是进行测试用例的资源初始化、
            test_XXX()：测试用例，把测试用例的步骤写在这、
            tearDown()：测试用例的资源释放,
            三个方法的执行顺序不变
            setUpClass()：给当前单元测试类的所有的用例进行初始化
            tearDownClass()：给当前单元测试类的所有的用例进行资源释放

            我是setUpClass方法
            我是setup方法
            我是加法的第一条测试用例
            我是tearDown方法
            我是tearDownClass方法
        4.创建测试用例：用test_开头的方法
        5.测试用例执行：
            main():
                执行所有的测试用例，执行顺序控制不了（按照方法名的字母顺序执行）
            testsuite（测试集合）解决上面的问题：
                1、创建testsuite对象
                2、调用testsuite中的方法addtest、addtests（）将测试加入测试集合
                3、testsuite的run（）方法运行测试集合，run方法的参数是testresult的对象：result = unittest.TestResult(),存储的是测试执行的结果(print(result.__dict__))
            testLoader:
                1.创建testloader对象
                2.loadertestsfromName（）将指定的测试用例加载到测试集合，并返回给测试对象，参数比较灵活：可以是模块名、类名、用例
                3.discover()方法：将指定模块中的测试用例一次性加载
                    suitt = unittest.defaultTestLoader.discover(r"", pattern="unit*.py")
                    path:指定存放测试用例的目录
                    pattern：指定匹配规则，very_reg_*.py
                                        very_login_*.py
            testRunner:
                之前测试执行的时候用的是run方法（suitt.run(result)哪个模块.run(TestResult)）,现在是TextTestRunner.run(哪个模块)
                TextTestRunner()->将结果以text文本形式展示的运行器
                第三方 HTMLTestRunner模块：将测试报告以HTML格式展示出来
                    1、下载该模块的Python3版本
                    2、复制文件到Python安装目录的lib目录下
                    3、导包
    断言：一个测试用例，测试步骤、测试断言缺一不可
        unittest中提供的断言方法：（一个用例断言失败后不会中断测试）
            assertEqual(a,b,msg=''):判断a和b是否相等，如果相等，则断言成功，如果不相等，会断言失败，并且输出msg消息
            assertNotEqual(a,b,msg=''):a和b是否不相等
            assertTrue(a):a是否为true
            assertFalse(a):a是否为false
            assertIs(a，b，msg=''):a和b的内存地址是否相同
            assertIsNot(a，b，msg=''):a和b的内存地址是否不相同
            assertIsNone(a):判断a对象是不是空指针
            assertIsNotNone(a):判断a对象是不是不是空指针
            assertIn(a,b):判断a是否是b的成员
            assertNotIn(a,b):判断a是否不是b的成员
            assertIsInstance(a,b):判断a是否是b的一个实例对象
            assertIsNotInstance(a,b):判断a是否不是b的一个实例对象
"""
import unittest
import myMath


class unitMyMath(unittest.TestCase):

    # 类方法
    @classmethod
    def setUpClass(cls):
        print("我是setUpClass方法")

    @classmethod
    def tearDownClass(cls):
        print("我是tearDownClass方法")

    # 方法名不能改，self参数不能少
    def setUp(self):
        print("我是setup方法")
        self.mm = myMath.myMath()

    # 必须是test开头的方法，这是一个测试用例
    def test_add_1(self):
        print("我是加法的第一条测试用例")
        # mm = myMath.myMath()
        addValue = self.mm.add(1, 1)
        expectVal = 2
        self.assertEqual(addValue, expectVal, "预期结果和实际结果不相等")

    def test_add_2(self):
        print("我是加法的第二条测试用例")
        # mm = myMath.myMath()
        addValue = self.mm.add("abc", "123")
        expectVal = "abc123"
        self.assertEqual(addValue, expectVal, "预期结果和实际结果不相等")

    # 方法名不能改，self参数不能少
    def tearDown(self):
        print("我是tearDown方法")


if __name__ == "__main__":
    # 调用执行单元测试类,通过主方法main执行,执行全部的测试用例
    # unittest.main()

    #     suite = unittest.TestSuite()
    #     # 追加测试用例到测试集合中，格式，类名：用例名
    #     suite.addTest(unitMyMath("test_add_2"))
    # #     运行
    #     result = unittest.TestResult()
    #     suite.run(result)
    #     print(result.__dict__)

    # 创建TestLoader对象
    loader = unittest.TestLoader()
    # suitt = loader.loadTestsFromName("unitMyMath.unityMyMath")

    # 模块名.类名.用例名
    # suitt = loader.loadTestsFromName("unitMyMath.unitMyMath.test_add_2")

    # TestLoader中discover方法加载用例。第一个参数是一个目录（目录如果有存放单元测试用例（unittest框架）则执行run，否则不会执行run，而且直接执行测试用例）,第二个参数是文件名的条件
    suitt = unittest.defaultTestLoader.discover(r"", pattern="unit*.py")

    # result = unittest.TestResult()
    # suitt.run(result)
    # print(result.__dict__)

    #使用TextTestRunner（）运行器提供的run（）方法测试集合
    #报告以textTestResult的形式展示的；TextTestRunner（）是TestRunner的子类；
    #视频、图片等直接用w是写不进去的，只能b的形式读写，“rb/wb”
    with open(r"re.txt","w",encoding="utf-8") as f:
        runner = unittest.TextTestRunner(f,descriptions="单元测试报告执行",verbosity=2)
        runner.run(suitt)
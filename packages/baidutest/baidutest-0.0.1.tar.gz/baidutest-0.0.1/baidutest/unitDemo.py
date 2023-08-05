import unittest
import myMath
import time
import os
from HTMLTestRunner import HTMLTestRunner

class unitTest(unittest.TestCase):
    def setUp(self):
        self.mm = myMath.myMath()
    def test_add_1(self):
        '''验证加法运算'''
        trueAdd = self.mm.add(2, 2)
        expectAdd = 4
        self.assertEqual(trueAdd,expectAdd,msg="实际结果与预期结果不一样")
    def tearDown(self):
        pass
if __name__ == "__main__":
    discover = unittest.defaultTestLoader.discover(r"", pattern="unitDemo.py")
    fileName = time.strftime("%Y-%m-%d-%H-%M-%S")+r".html"
    path = os.path.dirname(__file__) + r"/"
    fileName = path + fileName
    with open(fileName,"wb") as f:
        # runner = unittest.TextTestRunner(f,verbosity=2)
        runner = HTMLTestRunner(f,verbosity=2,title="HTML版的单元测试报告",description="")
        runner.run(discover)


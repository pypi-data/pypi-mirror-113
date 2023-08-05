import time


# try:
#     x = int(input("请输入一个数字: "))
# except:
#     print("您输入的不是数字，请再次尝试输入！")


def search(driver,val):
    # 打开百度首页
    driver.get("https://www.baidu.com")
    # 在百度的文本框中输入selenium
    driver.find_element_by_id("kw").send_keys(val)
    # 点击百度按钮
    driver.find_element_by_id("su").click()
    time.sleep(5)
    # 关闭浏览器
    driver.quit()


if __name__ == '__main__':
    # 导包
    # from selenium import webdriver
    #
    # # 创建浏览器对象
    # driver = webdriver.Firefox()
    # # 键入的值
    # val = "When I See You Again"
    # search(driver, val)

    a=1
    print(type(a))
    print(type(str(a)))
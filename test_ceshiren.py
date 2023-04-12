import time

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
# 测试类，需要用Test开头
# 需要继承的时，Class后面才需要加括号
# self是python语法，如果是类里面的函数（方法）
# 第一个参数就是指向自己，如果在类中的函数必须这样写，除非使用其他装饰器，如 @stastic
class TestCeshiren:
# 前置处理：用例执行之前的操作
    # 测试类中的所有用例执行之前的操作，仅执行一次
    def setup_class(self):
        # 返回一个浏览器对象，提供浏览器相关的操作 self.driver则可以操作浏览器，如前进后退等
        self.driver = webdriver.Chrome()
        # 配置隐式等待，查找元素时，若出现NoSuchElementException，不会直接报错，而是轮询继续查找，最多等待t
        # 隐式等待是全局的
        self.driver.implicitly_wait(3)
    # 每个测试用例、方法执行之前都会执行它，有多少用例执行几次
    def setup(self):
        # 1、打开网页
        # get可以打开网页
        self.driver.get("https://ceshiren.com/")
        # 强制等待
        # time.sleep(3)
# 后置处理：用例执行之后的操作
    # 测试类中的所有用例执行之后的操作
    def teardown_class(self):
        # 关闭浏览器进程
        self.driver.quit()
#冒烟案例
    # 函数命名规范：test_功能模块
    def test_search(self):
        """
        先梳理测试步骤，然后按照测试步骤实现，
        【测试步骤】
        1、打开ceshiren网站
        2、打开首页的搜索按钮
        3、点击高级搜索按钮
        4、输入搜索信息
        5、点击搜索
        6、断言搜索的信息和结果是相关的
        """
    # 2、打开首页的搜索按钮（查找方式，具体的元素信息）
        # find_element可以用来找元素，返回值是操作的元素对象，可以直接.调用相关方法进行操作
        # 定位时有ID优先使用ID，但是有些ID 是动态变化的
        self.driver.find_element(By.ID, "search-button").click()
    # 3、点击高级搜索按钮
        # 绝对定位不容易维护
        # 先在元素上单击右键，选择检查获取class，然后在console里面输入CSS表达式检查是否能找到，如$(."search-input") + enter
        # 若有返回，且length不为0则说明可以找到
        self.driver.find_element(By.CSS_SELECTOR, ".searching").click()
    # 4、输入搜索信息
        self.driver.find_element(By.CSS_SELECTOR, ".full-page-search").send_keys("git")
    # 5、点击搜索
        self.driver.find_element(By.CSS_SELECTOR, ".search-cta").click()
    # 6、断言——搜索的信息和结果需要是相关的
        # find_elemnent找到多个时，默认返回第一个
        # 先加强制等待执行，确认时什么原因导致报错，如果加了之后不报错，说明这个报错是因为没加载出来导致的
        # 如果因为没加载出来导致找不到元素，可以加隐式等待，然后去掉强制等待
        res_text = self.driver.find_element(By.CSS_SELECTOR, ".topic-title").text

        # 截图操作
        self.driver.save_screenshot("image1.png")
        # 塞入报告，需要使用命令行的方式在当前目录执行 pytest .\test_ceshiren.py --alluredir=./report
        # 查看报告： allure serve ./report 报告名称
        allure.attach.file("image1.png", name="SmokeTest", attachment_type=allure.attachment_type.PNG)
        # 判断获取到的搜索结果的文本是否包含git

        assert "git" in res_text
# 异常情况用例，输入内容为空
    def test_search_null(self):
        """
        先梳理测试步骤，然后按照测试步骤实现，
        测试步骤
        1、打开ceshiren网站
        2、打开首页的搜索按钮
        3、点击高级搜索按钮
        4、输入搜索信息
        5、点击搜索
        6、断言搜索的信息和结果是相关的
        """
        # self.driver.get("https://ceshiren.com/")
        self.driver.find_element(By.ID, "search-button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".searching").click()
        self.driver.find_element(By.CSS_SELECTOR, ".full-page-search").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, ".search-cta").click()
        res_text = self.driver.find_element(By.CSS_SELECTOR, ".fps-invalid").text
        self.driver.save_screenshot("image_null.png")
        allure.attach.file("image_null.png", name="NullResult", attachment_type=allure.attachment_type.PNG)
        assert res_text == "您的搜索词过短。"
# 异常情况用例，输入内容为特殊字符
    def test_search_special(self):
        """
        先梳理测试步骤，然后按照测试步骤实现，
        测试步骤
        1、打开ceshiren网站
        2、打开首页的搜索按钮
        3、点击高级搜索按钮
        4、输入搜索信息
        5、点击搜索
        6、断言搜索的信息和结果是相关的
        """
        # self.driver.get("https://ceshiren.com/")
        self.driver.find_element(By.ID, "search-button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".searching").click()
        self.driver.find_element(By.CSS_SELECTOR, ".full-page-search").send_keys(".////")
        self.driver.find_element(By.CSS_SELECTOR, ".search-cta").click()
        res_text = self.driver.find_element(By.CSS_SELECTOR, ".loading-container").text
        self.driver.save_screenshot("image_noResult.png")
        allure.attach.file("image_noResult.png", name="NoResult", attachment_type=allure.attachment_type.PNG)
        assert res_text == "找不到结果。\n找不到您要找的内容？ 尝试使用 Google 进行搜索：\nGoogle"



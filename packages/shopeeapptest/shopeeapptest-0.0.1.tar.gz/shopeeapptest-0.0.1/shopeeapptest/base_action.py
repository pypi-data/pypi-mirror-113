from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shopeeapptest.element_locator import ElementLocator
from selenium.common.exceptions import InvalidSelectorException


class BaseAction(object):

    def __init__(self, _driver: WebDriver):
        self.driver = _driver

    # 手指上滑动
    def swipe_up(self, t=500, n=1):
        """向上滑动屏幕"""
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5  # x坐标
        y1 = l['height'] * 0.75  # 起始y坐标
        y2 = l['height'] * 0.25  # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

    # 手指下滑动
    def swipe_down(self, t=500, n=1):
        """向下滑动屏幕"""
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5  # x坐标
        y1 = l['height'] * 0.25  # 起始y坐标
        y2 = l['height'] * 0.75  # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

    # 手指左滑动
    def swipe_left(self, t=500, n=1):
        """向左滑动屏幕"""
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.75
        y1 = l['height'] * 0.5
        x2 = l['width'] * 0.25
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    # 手指右滑动
    def swipe_right(self, t=500, n=1):
        """向右滑动屏幕"""
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.25
        y1 = l['height'] * 0.5
        x2 = l['width'] * 0.75
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    # 根据资源id发送按键操作
    def safe_send_keys_to_element_with_resource_id(self, resource_id, keys: str):
        ele = self.driver.find_element_by_id(resource_id)
        ele.send_keys(keys)

    # 获取context name列表
    def get_context_name_list(self):
        return self.driver.contexts

    # 根据context_name切换context
    def switch_context_by_name(self, context_name):
        self.driver.switch_to.context(context_name)

    # 滑动到指定元素
    def scroll_to_element_by_text(self, element_text):
        return self.driver.find_element_by_android_uiautomator(
            f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("{element_text}").instance(0));')

    # 滑动到顶部（最多滑动10次）
    def scroll_to_beginning(self):
        try:
            self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true)).scrollToBeginning(10)')
        except InvalidSelectorException:
            # 虽然 Appium 不允许您直接使用完整的“UIScrollable”功能，但可以忽略错误并执行此操作。
            pass

    # 滑动到底部（最多滑动10次）
    def scroll_to_end(self):
        try:
            self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true)).scrollToEnd(10)')
        except InvalidSelectorException:
            # 虽然 Appium 不允许您直接使用完整的“UIScrollable”功能，但可以忽略错误并执行此操作。
            pass

    # 向下滑动一下
    def scroll_forward(self):
        try:
            self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
        except InvalidSelectorException:
            # 虽然 Appium 不允许您直接使用完整的“UIScrollable”功能，但可以忽略错误并执行此操作。
            pass

    # 向上滑动一下
    def scroll_backward(self):
        try:
            self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true)).scrollBackward()')
        except InvalidSelectorException:
            # 虽然 Appium 不允许您直接使用完整的“UIScrollable”功能，但可以忽略错误并执行此操作。
            pass

    # 等待元素出现
    def wait_element_located(self, ele_locator: ElementLocator, timeout=10):
        WebDriverWait(self.driver, timeout, 0.5).until(
            EC.presence_of_element_located((ele_locator.by, ele_locator.locator)))

    # 等待元素可以点击
    def wait_element_clickable(self, ele_locator: ElementLocator, timeout=10):
        WebDriverWait(self.driver, timeout, 0.5).until(
            EC.element_to_be_clickable((ele_locator.by, ele_locator.locator)))

    # 等待元素可以点击的时候点击元素
    def click_when_element_clickable(self, ele_locator: ElementLocator, timeout=10):
        self.wait_element_clickable(ele_locator, timeout)
        self.find_element_and_click(ele_locator)

    # 等待元素出现并点击
    def wait_ele_located_and_click(self, ele_locator: ElementLocator, timeout=10):
        self.wait_element_located(ele_locator, timeout)
        self.driver.find_element(ele_locator.by, ele_locator.locator).click()

    # 等待元素出现并输入
    def wait_ele_located_and_send_keys(self, keys, ele_locator: ElementLocator, timeout=10):
        self.wait_element_located(ele_locator, timeout)
        self.driver.find_element(ele_locator.by, ele_locator.locator).send_keys(keys)

    # 寻找元素
    def find_element(self, ele_locator: ElementLocator):
        return self.driver.find_element(ele_locator.by, ele_locator.locator)

    # 寻找元素并点击
    def find_element_and_click(self, ele_locator: ElementLocator):
        return self.driver.find_element(ele_locator.by, ele_locator.locator).click()

    # 寻找元素并输入
    def find_element_and_send_keys(self, keys, ele_locator: ElementLocator):
        return self.driver.find_element(ele_locator.by, ele_locator.locator).send_keys(keys)

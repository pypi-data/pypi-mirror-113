from appium.webdriver.common.mobileby import MobileBy


# 元素定位器
class ElementLocator:

    def __init__(self, locator, by=MobileBy.XPATH, name=None):
        self.locator = locator
        self.by = by
        self.name = name

    def __str__(self):
        return f'{self.locator}-{self.by}-{self.name}'

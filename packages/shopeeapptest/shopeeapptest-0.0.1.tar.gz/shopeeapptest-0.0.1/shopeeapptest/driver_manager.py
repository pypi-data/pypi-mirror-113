from appium import webdriver


class DriverManager:
    def __init__(self, appnium_server_url, udid, system_port, device_name=None, version="7.1.1"):
        # self.server_url = f'http://{host}:4723/wd/hub'
        self.server_url = appnium_server_url
        self.version = version
        self.udid = udid
        self.system_port = system_port
        if device_name is None:
            self.device_name = udid
        else:
            self.device_name = device_name

    # 获取app web driver，需要传入需要启动的app包以及对应的启动页面
    def get_driver(self, app_package=None, open_page=None):
        desired_capabilities = {
            # 'app': "/Users/liangtan/Downloads/app-debug.apk",
            # 'appActivity': OPEN_PAGE,
            'platformName': 'Android',
            'platformVersion': self.version,  # 6.0.1
            'deviceName': self.device_name,  # d5ce3e7  localhost:5555
            'automationName': 'UiAutomator2',
            'newCommandTimeout': 3600,
            'disableAndroidWatchers': True,
            'noReset': True,
            'udid': self.udid,
            'systemPort': self.system_port  # '8201'
        }
        if app_package:
            desired_capabilities.setdefault('appPackage', app_package)
        if open_page:
            desired_capabilities.setdefault('appActivity', open_page)
        driver = webdriver.Remote(command_executor=self.server_url, desired_capabilities=desired_capabilities)
        driver.implicitly_wait(60)
        return driver

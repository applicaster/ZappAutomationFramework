
from time import sleep
from src.utils.logger import Logger
from src.configuration.configuration import Configuration
from src.global_defines import BrowserTypes, RemoteControlKeys
from src.utils.print import PRINT
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from src.automation_manager.automation_driver import AutomationDriver


"""
Global Defines
"""
WINDOW_DEFAULT_WIDTH_SIZE = 1920
WINDOW_DEFAULT_HEIGHT_SIZE = 1080


class SeleniumWebDriver(AutomationDriver):
    """
    Public Implementation
    """

    def find_element_by_accessibility_id(self, accessibility_id, retries=1):
        Logger.get_instance().info(self, 'find_element_by_accessibility_id',
                                   'search for "%s"' % accessibility_id)
        element = None
        for i in range(retries):
            try:
                element = self.driver_.find_element_by_id(accessibility_id)
            except Exception:
                Logger.get_instance().errorLogger.get_instance().warning(
                    self,
                    'find_element_by_accessibility_id',
                    'Could not find element with id: %s' % accessibility_id
                )

        return element

    def is_element_focused(self, accessibility_id):
        element = self.find_focused_element()

        if element is None:
            return False

        return element.get_attribute('data-testid') == accessibility_id

    def find_focused_element(self):
        Logger.get_instance().info(self, 'find_focused_element', '')
        element = None
        try:
            element = self.driver_.find_element_by_css_selector(
                'div[focused-teststate="focused"]')

        except Exception:
            Logger.get_instance().error(
                self,
                'find_element_by_css_selector',
                'Could not find current focused element'
            )

        return element

    def find_element_by_css_selector(self, css_selector):
        Logger.get_instance().info(self, 'find_element_by_css_selector',
                                   'search for "%s"' % css_selector)
        element = None
        try:
            element = self.driver_.find_element_by_css_selector(
                'div[data-testid="%s"]' % css_selector)

        except Exception:
            Logger.get_instance().warning(
                self,
                'find_element_by_css_selector',
                'Could not find element with css selector: %s' % css_selector
            )

        return element

    def find_element_by_text(self, text, retries=1):
        Logger.get_instance().info(self, 'find_element_by_text', 'search for: "%s"' % text)

        element = None
        for i in range(retries):
            try:
                element = self.driver_.find_element_by_xpath(
                    "//*[contains(text(), '%s')]" % text)
            except Exception:
                Logger.get_instance().warning(
                    self,
                    'find_element_by_text',
                    'Could not find element with text: "%s"' % text
                )

        return element

    def activate_app(self, bundle_id=None, app_package=None):
        Logger.get_instance().info(self, 'activate_app',
                                   'Selenium driver will load url with address %s' % self.url_)
        self.__setup_selenium_web_driver__()
        self.driver_.get(self.url_)

    def terminate_app(self):
        Logger.get_instance().info(self, 'terminate_app', 'Selenium driver will terminate')
        self.driver_.quit()

    def connect(self, retries=1):
        # 'Connecting performed when activating tha app'
        pass

    def disconnect(self):
        self.driver_.quit()

    def send_keys(self, keys, time_out=0.5):
        PRINT('Send remote control keys: %s' % str(keys), text_color='cyan')
        if isinstance(keys, str):
            self.__send_key__(keys)
            self.wait(time_out)

        elif isinstance(keys, type([])):
            for key in keys:
                if isinstance(key, int):
                    self.wait(key)
                else:
                    self.__send_key__(key)
                    self.wait(time_out)

    def wait(self, seconds):
        sleep(seconds)

    def take_screenshot(self, file_path):
        self.driver_.save_screenshot(file_path)

    def get_device_log(self):
        return self.driver_.get_log('browser')

    def refresh(self):
        self.driver_.refresh()

    def get_dom_tree(self):
        return self.driver_.execute_script("return document.documentElement.outerHTML")

    """
    Private Implementation
    """

    def __setup_window_size__(self):
        width = Configuration.get_instance().get('selenium', 'screen_width')
        width = WINDOW_DEFAULT_WIDTH_SIZE if width is None else width

        height = Configuration.get_instance().get('selenium', 'screen_height')
        height = WINDOW_DEFAULT_HEIGHT_SIZE if height is None else height

        self.driver_.set_window_size(width, height)

    def __setup_selenium_web_driver__(self):
        if self.browser_ == BrowserTypes.CHROME:
            self.driver_ = webdriver.Chrome('chromedriver')

        self.__setup_window_size__()
        self.actions_ = ActionChains(self.driver_)

    def __send_key__(self, key):
        action = ActionChains(self.driver_)
        action.send_keys(self.__convert_key_code__(key))
        action.perform()

    def __convert_key_code__(self, key_code):
        if key_code == RemoteControlKeys.RIGHT:
            return Keys.RIGHT

        if key_code == RemoteControlKeys.LEFT:
            return Keys.LEFT

        if key_code == RemoteControlKeys.UP:
            return Keys.UP

        if key_code == RemoteControlKeys.DOWN:
            return Keys.DOWN

        if key_code == RemoteControlKeys.BACK:
            return Keys.BACKSPACE

        if key_code == RemoteControlKeys.ENTER:
            return Keys.ENTER

    def __init__(self, url, browser):
        self.driver_ = None
        self.url_ = url
        self.browser_ = browser

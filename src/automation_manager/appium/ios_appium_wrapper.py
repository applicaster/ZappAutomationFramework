
from src.automation_manager.appium.base_appium_wrapper import BaseAppiumWrapper
from appium.webdriver.common.mobileby import MobileBy
from src.utils.logger import Logger
from src.automation_manager.appium.base_appium_wrapper import FINDING_ELEMENT_BY_TEXT
from src.global_defines import RemoteControlKeys, PlatformType
from src.configuration.configuration import Configuration


class AppleTvRemoteControlKeyCodes:
    MENU = 'Menu'
    UP = 'Up'
    DOWN = 'Down'
    RIGHT = 'Right'
    LEFT = 'Left'
    HOME = 'Home'
    PLAY_PAUSE = 'playpause'
    SELECT = 'Select'


class IosAppiumWrapper(BaseAppiumWrapper):
    """
    Public Implementation
    """
    def find_element_by_text(self, text, retries=1):
        exception_message = None
        for i in range(retries):
            try:
                return self.driver_.find_element(MobileBy.IOS_PREDICATE, "name == '" + text + "'")
            except Exception as exception:
                exception_message = exception.msg

            try:
                return self.driver_.find_element_by_name(text)
            except Exception as exception:
                exception_message = exception.msg

            try:
                return self.driver_.find_element_by_xpath('//*[contains(@name, "%s")]' % text)
            except Exception as exception:
                exception_message = exception.msg

            self.wait(1)

        Logger.get_instance().warning(self, "find_element_by_text", FINDING_ELEMENT_BY_TEXT % str(text))
        Logger.get_instance().warning(self, "find_element_by_text", exception_message)
        return None

    def __send_key__(self, key_code):
        if Configuration.get_instance().platform_type() == PlatformType.TV_OS:
            self.driver_.execute_script('mobile: pressButton', {'name': self.__convert_tv_os_key_code__(key_code)})

    def __convert_ios_key_code__(self, key_code):
        return key_code

    def __convert_tv_os_key_code__(self, key_code):
        switcher = {
            RemoteControlKeys.MENU:
                AppleTvRemoteControlKeyCodes.MENU,

            RemoteControlKeys.UP:
                AppleTvRemoteControlKeyCodes.UP,

            RemoteControlKeys.DOWN:
                AppleTvRemoteControlKeyCodes.DOWN,

            RemoteControlKeys.LEFT:
                AppleTvRemoteControlKeyCodes.LEFT,

            RemoteControlKeys.RIGHT:
                AppleTvRemoteControlKeyCodes.RIGHT,

            RemoteControlKeys.BACK:
                AppleTvRemoteControlKeyCodes.MENU,

            RemoteControlKeys.HOME:
                AppleTvRemoteControlKeyCodes.HOME,

            RemoteControlKeys.ENTER:
                AppleTvRemoteControlKeyCodes.SELECT,

            RemoteControlKeys.PLAY_PAUSE:
                AppleTvRemoteControlKeyCodes.PLAY_PAUSE
        }
        return switcher[key_code] if key_code in switcher.keys() else key_code

    def accept_alert_message(self, timeout=5):
        for i in range(timeout):
            try:
                self.driver_.switch_to.alert.accept()
                break
            except Exception:
                self.wait(1)

        self.wait(1)

    def dismiss_alert_message(self, timeout=5):
        for i in range(timeout):
            try:
                self.driver_.switch_to.alert.dismiss()
                break
            except Exception:
                self.wait(1)

        self.wait(1)

    def get_device_log(self):
        """
        Gets the log for a given log type
        """
        return self.driver_.get_log('syslog')

    """
    Private Implementation
    """
    def __init__(self, desired_capabilities, appium_server_host):
        BaseAppiumWrapper.__init__(self, desired_capabilities, appium_server_host)

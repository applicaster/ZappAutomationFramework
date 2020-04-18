
from src.automation_manager.appium.base_appium_wrapper import BaseAppiumWrapper
from appium.webdriver.common.mobileby import MobileBy
from src.utils.logger import Logger
from src.automation_manager.appium.base_appium_wrapper import FINDING_ELEMENT_BY_TEXT


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


import pytest
from src.configuration.configuration import Configuration
from src.global_defines import PlatformType

from src.automation_manager.appium.ios_appium_wrapper import IosAppiumWrapper
from src.automation_manager.appium.android_appium_wrapper import AndroidAppiumWrapper
from src.automation_manager.selenium.selenium_wrapper import SeleniumWebDriver
from src.automation_manager.automation_driver import AutomationDriver


class AutomationManager(object):
    __instance = None

    """
    Public Implementation
    """
    @staticmethod
    def get_instance():
        """ Static access method. """
        if AutomationManager.__instance is None:
            AutomationManager()

        return AutomationManager.__instance

    def get_driver(self) -> AutomationDriver:
        return self.automation_driver_

    """
    Private Implementation
    """
    def __setup_automation_driver__(self):
        platform = Configuration.get_instance().platform_type()

        if platform in (PlatformType.ANDROID, PlatformType.ANDROID_TV, PlatformType.IOS, PlatformType.TV_OS):
            self.__setup_driver_based_appium__()

        elif platform == PlatformType.WEB:
            self.__setup_driver_based_selenium__()

        if Configuration.get_instance().get('appium', 'autoLaunch') is False:
            self.automation_driver_.connect()

    def __setup_driver_based_selenium__(self):
        url = Configuration.get_instance().get('selenium', 'url')
        browser = Configuration.get_instance().get('selenium', 'browser')
        self.automation_driver_ = SeleniumWebDriver(url, browser)

    def __setup_driver_based_appium__(self):
        configuration = Configuration.get_instance()
        appium_server_host = configuration.get('appium', 'host')
        desired_capabilities = configuration.get_section('appium')
        desired_capabilities.pop('host', None)

        if configuration.platform_type() == PlatformType.IOS:
            desired_capabilities['platformName'] = 'iOS'
            self.automation_driver_ = IosAppiumWrapper(desired_capabilities, appium_server_host)

        elif configuration.platform_type() == PlatformType.TV_OS:
            desired_capabilities['platformName'] = 'tvOS'
            self.automation_driver_ = IosAppiumWrapper(desired_capabilities, appium_server_host)

        elif configuration.platform_type() in (PlatformType.ANDROID, PlatformType.ANDROID_TV):
            desired_capabilities['platformName'] = 'Android'
            self.automation_driver_ = AndroidAppiumWrapper(desired_capabilities, appium_server_host)

    def __init__(self):
        """ Virtually private constructor. """
        if AutomationManager.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            AutomationManager.__instance = self
            self.__setup_automation_driver__()


@pytest.fixture(scope="class")
def automation_driver(request):
    # set a class attribute on the invoking test context
    request.cls.driver = AutomationManager.get_instance().get_driver()

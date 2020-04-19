
from appium import webdriver
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.configuration.configuration import Configuration
from time import sleep
from sys import exit
from src.global_defines import PlatformType
from src.automation_manager.automation_driver import AutomationDriver

'''
Global Defines
'''
DEFAULT_TAP_DURATION = 300
DEFAULT_SWIPE_DURATION = 500
APPIUM_CONNECT_RETIRES_NUM = 5
FAILED_CONNECTING_TO_APPIUM_SERVER = 'Fatal Error, test failed connecting with Appium server'
FAILED_ACTIVATING_APPLICATION = 'Fatal Error, test failed activating the application'
OPEN_CONNECTION_WITH_APPIUM_SERVER_SUCCEEDED = 'Opening connection with Appium server finished successfully'
MESSAGE_CLOSE_CONNECTION_WITH_APPIUM_SERVER = "Closing connection with Appium server finished successfully"
MESSAGE_IMPLEMENT_METHOD_IN_DERIVED_CLASS = "Function '%s' must be implemented in derived class"
FINDING_ELEMENT_BY_ACCESSIBILITY_ID = 'Appium failed finding element by accessibility id "%s"'
FINDING_ELEMENT_BY_TEXT = "Appium failed finding element by text '%s'"
ERROR_FAILED_ON_CLOSING_CONNECTION_WITH_APPIUM_SERVER = "Closing connection with Appium server failed"


class BaseAppiumWrapper(AutomationDriver):
    """
    Public Implementation
    """
    def activate_app(self,
                     bundle_id=Configuration.get_instance().get_bundle_id(),
                     app_package=Configuration.get_instance().get('appium', 'appActivity')):
        """
        # Activates an existing application on the device under test and moves it to the foreground.
        # The application should be already running in order to activate it.
        # The call is ignored if the application is already in foreground.
        # :param bundle_id: bundle id of the app you want to launch
        # :app_package: android only, the activity to start.
        # :return: App WebDriver session
        """
        platform = Configuration.get_instance().platform_type()

        if platform in (PlatformType.ANDROID, PlatformType.ANDROID_TV):
            return self.__activate_android_app__(bundle_id, app_package)

        if platform in (PlatformType.IOS, PlatformType.TV_OS):
            return self.__activate_ios_app__(bundle_id)

    def terminate_app(self, bundle_id=Configuration.get_instance().get_bundle_id()):
        """
        Terminates an existing application on the device.
        :param bundle_id: The bundle identifier of the application, which is going to be terminated. If bundle id is
        None test will take the one found in the configuration.
        :return: If the application is not running then the returned result will be false, otherwise true.
        """
        return self.driver_.terminate_app(bundle_id)

    def connect(self):
        """
        This method connects to the appium server.
        :return: None
        """
        for i in range(APPIUM_CONNECT_RETIRES_NUM):
            try:
                self.driver_ = webdriver.Remote(self.appium_server_host_, self.desired_capabilities_)
                if self.driver_ is not None:
                    break
            except Exception as exception:
                print(FAILED_CONNECTING_TO_APPIUM_SERVER)
                print(str(exception))
                self.driver_ = None
                self.wait(1)

        if self.driver_ is None:
            exit(FAILED_CONNECTING_TO_APPIUM_SERVER)

        return True

    def disconnect(self):
        """
        This method disconnects from appium server
        :return: None
        """
        return self.driver_.quit()

    def wait(self, seconds):
        sleep(seconds)

    def get_page_resource(self):
        """
        Get the current application hierarchy XML (app) or page source (web)
        """
        return self.driver_.page_source

    def get_window_rect(self):
        """
        Gets the x, y coordinates of the window as well as height and width of
        the current window.
        """
        return self.driver_.get_window_rect()

    def get_screenshot_as_base64(self):
        """
        Gets the screenshot of the current window as a base64 encoded string which is useful in embedded images in HTML.
        """
        return self.driver_.get_screenshot_as_base64()

    def take_screenshot(self, file_path):
        self.driver_.get_screenshot_as_file(file_path)

    def find_element_by_text(self, text, retries=1): raise NotImplementedError
    def get_device_log(self): raise NotImplementedError

    def find_element_by_accessibility_id(self, accessibility_id, retries=1):
        for i in range(retries):
            try:
                return self.driver_.find_element_by_accessibility_id(accessibility_id)
            except Exception as exception:
                Logger.get_instance().warning(self, 'find_element_by_accessibility_id',
                                              FINDING_ELEMENT_BY_ACCESSIBILITY_ID)
                self.wait(1)
        return None

    def send_keys(self, keys, time_out=0.5):
        PRINT('Send remote control keys: %s' % str(keys), text_color='cyan')
        if isinstance(keys, str):
            self.__send_key__(self.__convert_key_code__(keys))
            self.wait(time_out)

        elif isinstance(keys, type([])):
            for key in keys:
                if isinstance(key, int):
                    self.wait(key)
                else:
                    self.__send_key__(self.__convert_key_code__(key))
                    self.wait(time_out)

    """
    Private Implementation
    """
    def __activate_android_app__(self, bundle_id, app_package):
        for i in range(APPIUM_CONNECT_RETIRES_NUM):
            try:
                return self.driver_.start_activity(bundle_id, app_package)
            except Exception as exp:
                Logger.get_instance().error(self, 'activate_app', FAILED_ACTIVATING_APPLICATION)
                Logger.get_instance().error(self, 'activate_app', exp.msg)
                self.wait(1)
        raise Exception(FAILED_ACTIVATING_APPLICATION)

    def __activate_ios_app__(self, bundle_id):
        if Configuration.get_instance().platform_type() == PlatformType.TV_OS:
            # autoLaunch=false is not working for tvOS platform, as for that tvOS is being launched when connecting
            # to appium with autoLaunch=true, see bug: https://github.com/appium/appium/issues/14198
            return
        for i in range(APPIUM_CONNECT_RETIRES_NUM):
            try:
                return self.driver_.activate_app(bundle_id)
            except Exception as exp:
                Logger.get_instance().error(self, 'activate_app', FAILED_ACTIVATING_APPLICATION)
                Logger.get_instance().error(self, 'activate_app', exp.msg)
                self.wait(1)
        raise Exception(FAILED_ACTIVATING_APPLICATION)

    def __init__(self, desired_capabilities, appium_server_host):
        self.desired_capabilities_ = desired_capabilities
        self.appium_server_host_ = appium_server_host
        self.driver_ = None

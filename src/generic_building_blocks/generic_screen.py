
from src.configuration.configuration import Configuration
from src.global_defines import PlatformType
from src.utils.logger import Logger
from src.utils.print import PRINT

'''
Global Defines
'''
FAILED_TO_VERIFY_SCREEN = 'Failed to verify screens with id: "%s"'
DERIVED_CLASS_MISSING_IMPLEMENTATION = 'Your derived class which inheriting from class %s must override the method %s'
START_NAVIGATING_TO_SCREEN = 'Application start navigating to screens named %s and id %s'
FINISHED_NAVIGATING_TO_SCREEN = "Application finished navigating to screens named %s and id %s"
DEFAULT_SCREEN_LOAD_TIMEOUT = 3


class GenericScreen(object):
    """
    Public Implementation
    """
    def verify_in_screen(self, assert_on_fail=True, retries=1):
        Logger.get_instance().take_screenshot('verify_in_screen_' + str(self.id))

        element = None
        for i in range(retries):
            if Configuration.get_instance().platform_type() == PlatformType.WEB:
                element = self.test.driver.find_element_by_css_selector(self.id)
            else:
                element = self.test.driver.find_element_by_accessibility_id(self.id)

            if element is not None:
                break
            self.test.driver.wait(1)

        if element is None:
            if assert_on_fail:
                Logger.get_instance().log_assert(False, FAILED_TO_VERIFY_SCREEN % self.id, with_snapshot=True)
            else:
                return False

        return True

    def get_screen_id(self):
        PRINT(DERIVED_CLASS_MISSING_IMPLEMENTATION % ('GenericScreen', 'get_screen_id()'), 'red')
        raise NotImplementedError

    def navigate(self):
        PRINT(DERIVED_CLASS_MISSING_IMPLEMENTATION % ('GenericScreen', 'navigate()'), 'red')
        raise NotImplementedError

    def get_screen_type(self):
        PRINT(DERIVED_CLASS_MISSING_IMPLEMENTATION % ('GenericScreen', 'get_screen_type()'), 'red')
        raise NotImplementedError

    def get_displayed_screen_id(self):
        """
        The following method check against the app UI what is the current displayed screens.
        The method iterates building blocks screens array and check one by one if its showing on screens
        :return: screens id as String, None in case algorithm could not find what is the screens
        """
        for screen_name in self.test.building_blocks.screens:
            screen_id = self.test.building_blocks.screens[screen_name].id
            element = self.test.driver.find_element_by_accessibility_id(screen_id)
            if element and element.is_displayed() and element.is_enabled():
                return screen_id
        Logger.get_instance().error(self, 'get_displayed_screen_id', 'Failed on finding current displayed screen id')
        return None

    def get_displayed_screen_building_block(self):
        """
        The following method finds the current displayed building block for current displaying screen
        :return: building block object of current displayed screens
        """
        for screen_name in self.test.building_blocks.screens:
            element = self.test.driver.find_element_by_accessibility_id(self.test.building_blocks.screens[screen_name].id)
            if element and element.is_displayed() and element.is_enabled():
                return self.test.building_blocks.screens[screen_name]
        Logger.get_instance().error(self, 'get_displayed_screen_building_block', 'Failed on finding current displayed building block')
        return None

    def set_screen_loading_timeout(self, timeout):
        self.load_timeout_ = timeout

    def get_screen_loading_timeout(self):
        return self.load_timeout_

    """
    Private Implementation
    """
    def __setup_generic_screen__(self):
        self.type = self.get_screen_type()
        self.id = self.get_screen_id()

    def __init__(self, test):
        self.test = test
        self.__setup_generic_screen__()
        self.load_timeout_ = DEFAULT_SCREEN_LOAD_TIMEOUT

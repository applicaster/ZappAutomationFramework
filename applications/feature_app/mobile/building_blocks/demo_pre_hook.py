

from src.generic_building_blocks.mobile.screens.mobile_screen import MobileScreen
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.global_defines import ScreenType


"""
Class Defines
"""
SUCCESS_BUTTON_TITLE = 'success_button'
ERROR_BUTTON_TITLE = 'error_button'
CANCEL_BUTTON_TITLE = 'cancel_button'
DEMO_HOOK_SCREEN_ID = 'quick_brick_hook_test'


class DemoPreHook(MobileScreen):
    """
    Public Implementation
    """
    def enter_with_success(self):
        self.__press_element_by_title__(SUCCESS_BUTTON_TITLE)

    def enter_with_error(self):
        self.__press_element_by_title__(ERROR_BUTTON_TITLE)

    def cancel_enter(self):
        self.__press_element_by_title__(CANCEL_BUTTON_TITLE)

    def get_screen_id(self):
        return DEMO_HOOK_SCREEN_ID

    def get_screen_type(self):
        return ScreenType.STANDALONE_SCREEN

    """
    Private Implementation
    """
    def __press_element_by_title__(self, title):
        element = self.test.driver.find_element_by_accessibility_id(title, retries=3)
        Logger.get_instance().log_assert(element, 'Element with title %s not found on the demo pre hook screen' % title)
        PRINT('     Test will press on "%s" button in the demo pre hook screen' % title)
        element.click()

    def __init__(self, test):
        MobileScreen.__init__(self, test)



from src.generic_building_blocks.mobile.screens.mobile_screen import MobileScreen
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.global_defines import ScreenType
from src.generic_building_blocks.generic_screen import FAILED_TO_VERIFY_SCREEN

"""
Class Defines
"""
SUCCESS_BUTTON_TITLE = 'Success'
ERROR_BUTTON_TITLE = 'Error'
CANCEL_BUTTON_TITLE = 'Cancel'


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
        return 'Quick Brick Hooks test'

    def get_screen_type(self):
        return ScreenType.STANDALONE_SCREEN

    """
    Private Implementation
    """
    def __press_element_by_title__(self, title):
        element = self.test.driver.find_element_by_text(title, retries=3)
        Logger.get_instance().log_assert(element, 'Element with title %s not found on the demo pre hook screen' % title)
        PRINT('     Test will press on "%s" button in the demo pre hook screen' % title)
        element.click()

    def __init__(self, test):
        MobileScreen.__init__(self, test)

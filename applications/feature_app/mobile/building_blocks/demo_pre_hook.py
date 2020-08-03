

from src.generic_building_blocks.mobile.screens.mobile_screen import MobileScreen
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.global_defines import ScreenType


"""
Class Defines
"""
SUCCESS_BUTTON_ACCESSIBILITY_IDENTIFIER = 'success_button'
ERROR_BUTTON_ACCESSIBILITY_IDENTIFIER = 'error_button'
CANCEL_BUTTON_ACCESSIBILITY_IDENTIFIER = 'cancel_button'
DEMO_HOOK_SCREEN_ACCESSIBILITY_IDENTIFIER = 'quick_brick_hook_test'


class DemoPreHook(MobileScreen):
    """
    Public Implementation
    """
    def enter_with_success(self):
        self.__press_element_by_id__(SUCCESS_BUTTON_ACCESSIBILITY_IDENTIFIER)

    def enter_with_error(self):
        self.__press_element_by_id__(ERROR_BUTTON_ACCESSIBILITY_IDENTIFIER)

    def cancel_enter(self):
        self.__press_element_by_id__(CANCEL_BUTTON_ACCESSIBILITY_IDENTIFIER)

    def get_screen_id(self):
        return DEMO_HOOK_SCREEN_ACCESSIBILITY_IDENTIFIER

    def get_screen_type(self):
        return ScreenType.STANDALONE_SCREEN

    """
    Private Implementation
    """
    def __press_element_by_id__(self, accessibility_identifier):
        element = self.test.driver.find_element_by_accessibility_id(accessibility_identifier, retries=3)
        Logger.get_instance().log_assert(
            element,
            'Element with id "%s" not found on the demo pre hook screen' % accessibility_identifier
        )
        PRINT('     Test will press on "%s" button in the demo pre hook screen' % accessibility_identifier)
        element.click()

    def __init__(self, test):
        MobileScreen.__init__(self, test)

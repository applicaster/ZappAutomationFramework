
from src.global_defines import ScreenType
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.data_providers.rivers_data_provider import RiversDataProvider
from src.generic_building_blocks.generic_screen import START_NAVIGATING_TO_SCREEN, FINISHED_NAVIGATING_TO_SCREEN
from src.generic_building_blocks.mobile.screens.mobile_screen import MobileScreen
from selenium.webdriver.common.keys import Keys

"""
Global Defines
"""
SCREEN_LOADING_TIMEOUT = 2
ENTER = 66


class SearchScreen(MobileScreen):
    AccessibilityIdentifierSearchArea = 'search_text_area'

    """
    Public Implementation
    """
    def get_screen_id(self):
        return 'search_screen'

    def get_screen_type(self):
        return ScreenType.STANDALONE_SCREEN

    def open_keyboard(self):
        if self.test.driver.is_keyboard_shown():
            return

        self.__get_search_area_element__().click()

    def close_keyboard(self):
        if self.test.driver.is_keyboard_shown():
            element = self.__get_search_area_element__()
            self.test.driver.tap_by_coordinates(element.location['x'], element.location['y'] + 200)

    def search(self, text):
        element = self.__get_search_area_element__()
        element.send_keys(text)

    def press_enter_in_search(self):
        self.test.driver.send_keys(ENTER)

    def set_loading_timeout(self, timeout):
        self.loading_timeout = timeout

    """
    Private Implementation
    """
    def __get_search_area_element__(self):
        return self.test.driver.find_element_by_accessibility_id(self.AccessibilityIdentifierSearchArea)

    def __init__(self, test):
        self.loading_timeout = SCREEN_LOADING_TIMEOUT
        MobileScreen.__init__(self, test)

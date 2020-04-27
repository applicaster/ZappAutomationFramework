
from src.utils.logger import Logger

"""
Global Defines
"""
ERROR_SPECIAL_BUTTON_NOT_FOUND_ON_SCREEN = 'nav_bar_left_icon not found on the screen'


class NavigationBar(object):
    AccessibilityIdentifierSpecialButton = 'nav_bar_left_icon'
    """
    Public Implementation
    """
    def press_menu_button(self):
        self.__press_nav_bar_left_button__()

    def press_back_button(self):
        self.__press_nav_bar_left_button__()

    """
    Private Implementation 
    """
    def __init__(self, test):
        self.test = test
        self.__setup_navigation_bar__()

    def __get_special_button_element__(self, retries=5):
        return self.test.driver.find_element_by_accessibility_id(
            self.AccessibilityIdentifierSpecialButton, retries=retries
        )

    def __press_nav_bar_left_button__(self):
        nav_bar_left_btn_element = self.__get_special_button_element__()
        Logger.get_instance().log_assert(nav_bar_left_btn_element, ERROR_SPECIAL_BUTTON_NOT_FOUND_ON_SCREEN)
        nav_bar_left_btn_element.click()

    def __setup_navigation_bar__(self):
        pass

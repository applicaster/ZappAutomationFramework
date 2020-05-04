
from src.utils.logger import Logger
from src.data_providers.rivers_data_provider import RiversDataProvider
"""
Global Defines
"""
ERROR_SPECIAL_BUTTON_NOT_FOUND_ON_SCREEN = 'nav_bar_left_icon not found on the screen'
LEFT_ICON_ANIMATION_TIMEOUT = 1.5
RIGHT_ICON_ANIMATION_TIMEOUT = 5


class NavigationBar(object):
    AccessibilityIdentifierSpecialButton = 'nav_bar_left_icon'
    """
    Public Implementation
    """
    def press_menu_button(self):
        self.__press_nav_bar_left_button__()
        self.test.driver.wait(LEFT_ICON_ANIMATION_TIMEOUT)

    def press_back_button(self):
        self.__press_nav_bar_left_button__()
        self.test.driver.wait(LEFT_ICON_ANIMATION_TIMEOUT)

    def press_right_button_by_position(self, position, screen_id=RiversDataProvider.get_instance().get_home_node()['id']):
        right_navigation_items = self.rivers_data_provider_.get_navigation_bar_items_for_screen(screen_id)
        for item in right_navigation_items:
            if item['position'] == position:
                item_accessibility_id = item['id']
        self.test.driver.find_element_by_accessibility_id(item_accessibility_id, retries=5).click()
        self.test.driver.wait(RIGHT_ICON_ANIMATION_TIMEOUT)

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
        self.rivers_data_provider_ = RiversDataProvider.get_instance()

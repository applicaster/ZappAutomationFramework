
from src.generic_building_blocks.mobile.screens.mobile_screen import MobileScreen


class SideMenu(MobileScreen):
    """
    Public Implementation
    """
    def navigate_to_item(self, name, scroll_to_top=False):
        self.test.building_blocks.navigation_bar.press_menu_button()
        self.dismiss_react_native_yellow_console_box()
        element = self.search_for_item_by_text(name, scroll_to_top=scroll_to_top)
        element.click()

    """
    Private Implementation 
    """
    def __init__(self, test):
        self.test = test
        self.__setup_side_menu__()

    def __setup_side_menu__(self):
        pass

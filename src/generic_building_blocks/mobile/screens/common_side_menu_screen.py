
from src.global_defines import ScreenType
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.data_providers.rivers_data_provider import RiversDataProvider
from src.generic_building_blocks.generic_screen import START_NAVIGATING_TO_SCREEN, FINISHED_NAVIGATING_TO_SCREEN
from src.generic_building_blocks.mobile.screens.mobile_screen import MobileScreen

"""
Global Defines
"""
SCREEN_LOADING_TIMEOUT = 2


class CommonSideMenuScreen(MobileScreen):
    """
    Public Implementation
    """
    def get_screen_id(self):
        river_data = RiversDataProvider.get_instance().get_data()
        for node in river_data:
            if 'name' in node and 'id' in node and node['name'].lower() == self.screen_name.lower():
                return node['id']

    def get_screen_type(self):
        return ScreenType.UI_BUILDER_SCREEN

    def navigate(self, home_navigation=False, verify_in_screen=True):
        Logger.get_instance().info(self, 'navigate', START_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))
        PRINT('     Start navigating to screen "%s" from the side menu' % self.screen_name)

        self.test.building_blocks.side_menu.navigate_to_item(self.screen_name)
        if verify_in_screen:
            self.verify_in_screen(retries=5)

        self.test.driver.wait(self.get_screen_loading_timeout())
        PRINT('     Finished navigating to screen "%s"' % self.screen_name)
        Logger.get_instance().info(self, 'navigate', FINISHED_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))

    def set_loading_timeout(self, timeout):
        self.loading_timeout = timeout

    """
    Private Implementation
    """
    def __init__(self, test, screen_name):
        self.screen_name = screen_name
        self.loading_timeout = SCREEN_LOADING_TIMEOUT
        MobileScreen.__init__(self, test)

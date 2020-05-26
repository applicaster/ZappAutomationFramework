
from src.configuration.configuration import Configuration
from src.global_defines import PlatformType, ScreenType
from src.utils.logger import Logger
from src.data_providers.rivers_data_provider import RiversDataProvider
from src.generic_building_blocks.generic_screen import GenericScreen
from src.generic_building_blocks.generic_screen import START_NAVIGATING_TO_SCREEN
from src.generic_building_blocks.generic_screen import FINISHED_NAVIGATING_TO_SCREEN

'''
Defines
'''
SCREEN_LOADING_TIMEOUT = 2


class TvScreen(GenericScreen):
    """
    Public Implementation
    """
    def get_screen_id(self):
        top_menu_bar_items = RiversDataProvider.get_instance().get_top_menu_bar_tv_items(by_title=False)
        for item in top_menu_bar_items:
            if 'title' in item and item['title'] == self.screen_name and 'data' in item:
                return item['data']['target']

    def get_screen_type(self):
        return ScreenType.UI_BUILDER_SCREEN

    def navigate(self):
        Logger.get_instance().info(self, 'navigate', START_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))

        if Configuration.get_instance().platform_type() in (PlatformType.ANDROID_TV, PlatformType.TV_OS):
            self.test.driver.send_keys(self.navigation_steps, 2)
        else:
            self.test.driver.send_keys(self.navigation_steps)

        self.verify_in_screen(retries=5)
        self.test.driver.wait(self.loading_timeout)
        Logger.get_instance().info(self, 'navigate', FINISHED_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))

    def set_navigation_steps(self, navigation_steps):
        self.navigation_steps = navigation_steps

    """
    Private Implementation
    """
    def __init__(self, test, screen_name, navigation_steps=None):
        self.screen_name = screen_name
        GenericScreen.__init__(self, test)
        self.loading_timeout = SCREEN_LOADING_TIMEOUT
        self.navigation_steps = navigation_steps

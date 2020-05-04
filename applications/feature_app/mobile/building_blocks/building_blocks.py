
from src.generic_building_blocks.building_blocks_interface import BuildingBlocksInterface
from src.generic_building_blocks.mobile.navigations.navigation_bar import NavigationBar
from src.generic_building_blocks.mobile.navigations.side_menu import SideMenu
from src.generic_building_blocks.mobile.screens.common_side_menu_screen import CommonSideMenuScreen
from src.generic_building_blocks.mobile.screens.search_screen import SearchScreen
from src.data_providers.rivers_data_provider import RiversDataProvider
from applications.feature_app.feature_app_player import FeatureAppPlayer
from src.utils.print import PRINT

"""
Global Defines
"""
BOOT_TIMEOUT = 90


class BuildingBlocks(BuildingBlocksInterface):
    """
    Public Implementation
    """
    def boot_step(self):
        PRINT('Start waiting for home screen to load')
        home_screen = self.test.building_blocks.screens['Home']
        boot_status = home_screen.verify_in_screen(retries=BOOT_TIMEOUT, assert_on_fail=False)
        PRINT('Finished waiting for home screen to load with: %s' % 'Success' if boot_status else 'Failure')
        if not boot_status:
            raise Exception('Application failed launching to home screen correctly')

        self.test.driver.wait(5)

    """
    Private Implementation
    """
    def __setup_building_blocks__(self):
        # Setup navigation building blocks
        self.side_menu = SideMenu(self.test)
        self.navigation_bar = NavigationBar(self.test)

        # Setup the application side menu screens based on what found in river.json
        side_menu_screens = RiversDataProvider.get_instance().get_side_menu_items(by_title=False)
        for screen in side_menu_screens:
            if screen['title'] not in self.screens:
                self.screens[screen['title']] = CommonSideMenuScreen(self.test, screen['title'])

        # Setup internal screens
        self.screens['search_screen'] = SearchScreen(self.test)
        self.screens['player_screen'] = FeatureAppPlayer(self.test)
        self.screens['ListScreen'].set_screen_loading_timeout(5)
        self.screens['GridScreen'].set_screen_loading_timeout(5)

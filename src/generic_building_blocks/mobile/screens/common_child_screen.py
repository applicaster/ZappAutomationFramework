
from src.global_defines import ScreenType, PlatformType
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.configuration.configuration import Configuration
from src.data_providers.rivers_data_provider import RiversDataProvider
from src.generic_building_blocks.generic_screen import START_NAVIGATING_TO_SCREEN, FINISHED_NAVIGATING_TO_SCREEN
from src.generic_building_blocks.mobile.screens.mobile_screen import MobileScreen

'''
Global Defines
'''
SCREEN_LOADING_TIMEOUT = 2


class CommonChildScreen(MobileScreen):
    """
    Public Implementation
    """
    def get_screen_id(self):
        river_data = RiversDataProvider.get_instance().get_data()
        for node in river_data:
            if "name" in node and "id" in node and str(node['name']) == self.screen_name:
                return node["id"]

        return None

    def get_screen_type(self):
        return ScreenType.UI_BUILDER_SCREEN

    def navigate(self, home_navigation=False, verify_in_screen=False):
        Logger.get_instance().info(self, 'navigate', START_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))
        PRINT('     Start navigating to screen "%s" from the side menu' % self.screen_name)

        if home_navigation:
            self.test.building_blocks.screens['Home'].navigate()

        # Navigate to parent screen
        self.test.building_blocks.screens[self.parent_screen_name].navigate()

        # From within parent screen navigate to child screen
        self.test.driver.find_element_by_text(self.screen_name).click()

        if Configuration.get_instance().platform_type() == PlatformType.IOS and self.open_with_url_scheme_:
            '''
            Workaround: when we install a fresh Simulator, like we are doing in CI machine. We have a bug that the first
            call to url scheme to screen pops a pop up message that asking the user permissions to open the app.
            This accept_alert_message() drop the message.
            '''
            PRINT('     Wait for pop up alert message and accept it')
            self.test.driver.accept_alert_message()
            self.test.driver.accept_alert_message()

        if verify_in_screen:
            self.verify_in_screen(retries=5)

        self.test.driver.wait(self.loading_timeout)

        PRINT('     Finished navigating to screen "%s"' % self.screen_name)
        Logger.get_instance().info(self, 'navigate', FINISHED_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))

    def set_loading_timeout(self, timeout):
        self.loading_timeout = timeout

    '''
    Private Implementation
    '''
    def __init__(self, test, screen_name, parent_screen_name, open_with_url_scheme=False):
        self.screen_name = screen_name
        self.parent_screen_name = parent_screen_name
        self.loading_timeout = SCREEN_LOADING_TIMEOUT
        self.open_with_url_scheme_ = open_with_url_scheme
        MobileScreen.__init__(self, test)

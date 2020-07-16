

from src.utils.logger import Logger
from src.utils.print import PRINT
from src.global_defines import ScreenType
from src.global_defines import PlatformType
from src.configuration.configuration import Configuration
from src.generic_building_blocks.mobile.screens.common_side_menu_screen import CommonSideMenuScreen
from src.generic_building_blocks.mobile.screens.common_side_menu_screen import START_NAVIGATING_TO_SCREEN
from src.generic_building_blocks.mobile.screens.common_side_menu_screen import FINISHED_NAVIGATING_TO_SCREEN

"""
Class Defines
"""
PLATFORM = Configuration.get_instance().platform_type()
INTERSTITIAL_SCREEN_ID = 'Test mode' if PLATFORM == PlatformType.IOS else 'Test Ad'
CLOSE_INTERSTITIAL_ACCESSIBILITY_ID = 'Close Advertisement' if PLATFORM == PlatformType.IOS else 'ANDROID_TODO_ID'
CLOSE_BUTTON_CENTRE_X = 20
CLOSE_BUTTON_CENTRE_Y = 20
INTERSTITIAL_LOAD_TIMEOUT = 25
SCREEN_LOAD_TIMEOUT = 5


class AdvertisingScreen(CommonSideMenuScreen):
    """
    Public Implementation
    """
    def navigate(self, home_navigation=False, verify_in_screen=True):
        Logger.get_instance().info(self, 'navigate', START_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))
        PRINT('     Start navigating to screen "%s" from the side menu' % self.screen_name)

        self.test.building_blocks.side_menu.navigate_to_item(self.screen_name)
        self.test.driver.wait(SCREEN_LOAD_TIMEOUT)

        PRINT('     Finished navigating to screen "%s"' % self.screen_name)
        Logger.get_instance().info(self, 'navigate', FINISHED_NAVIGATING_TO_SCREEN % (self.screen_name, self.id))

    def close_interstitial(self):
        PRINT('     Start closing the interstitial')
        if PLATFORM == PlatformType.IOS:
            self.__press_element_by_title__(CLOSE_INTERSTITIAL_ACCESSIBILITY_ID)
        else:
            """
            Workaround:
            We have a limitation that not allowing us to add accessibility identifiers to the interstitial view of
            the Android app. Its forces us to press by coordinates the top left corner of the screen in order to close
            the adv.  
            """
            self.test.driver.wait(2)
            self.test.driver.tap_by_coordinates(CLOSE_BUTTON_CENTRE_X, CLOSE_BUTTON_CENTRE_Y)

        self.test.driver.wait(SCREEN_LOAD_TIMEOUT)
        PRINT('     Finished closing the interstitial')

    def verify_interstitial_is_displaying(self):
        """
        Workaround:
        We have a limitation that not allowing us to add accessibility identifiers to the interstitial view of
        the Android app. Its forces us to validate with "what we have on screen" from google. 
        """
        if PLATFORM == PlatformType.IOS:
            Logger.get_instance().log_assert(
                self.test.driver.find_element_by_text(INTERSTITIAL_SCREEN_ID, retries=INTERSTITIAL_LOAD_TIMEOUT) and
                self.test.driver.find_element_by_text(CLOSE_INTERSTITIAL_ACCESSIBILITY_ID, retries=INTERSTITIAL_LOAD_TIMEOUT),
                'Interstitial is not displaying on the screen'
            )
        else:
            Logger.get_instance().log_assert(
                self.test.driver.find_element_by_text(INTERSTITIAL_SCREEN_ID, retries=INTERSTITIAL_LOAD_TIMEOUT),
                'Interstitial is not displaying on the screen'
            )

    def verify_interstitial_is_not_displaying(self):
        Logger.get_instance().log_assert(
            not self.test.driver.find_element_by_text(INTERSTITIAL_SCREEN_ID, retries=3) and
            not self.test.driver.find_element_by_text(CLOSE_INTERSTITIAL_ACCESSIBILITY_ID, retries=3),
            'Interstitial once is displaying on the screen, when it should not'
        )

    def get_screen_type(self):
        return ScreenType.STANDALONE_SCREEN

    """
    Private Implementation
    """
    def __press_element_by_title__(self, title):
        element = self.test.driver.find_element_by_text(title, retries=3)
        Logger.get_instance().log_assert(element, 'Element with title "%s" not found on the screen' % title)
        PRINT('     Test will press on "%s" element ' % title)
        element.click()

    def __init__(self, test, screen_name):
        CommonSideMenuScreen.__init__(self, test, screen_name)

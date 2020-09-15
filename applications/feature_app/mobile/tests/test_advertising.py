
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Logger, Configuration
from src.global_defines import PlatformType

"""
Global Defines
"""
ADVERTISING_SCREEN = 'AdvertisingScreen'
INTERSTITIAL_ONCE_SCREEN = 'InterstitialOnceScreen'
INTERSTITIAL_SCREEN = 'InterstitialScreen'
ADVERTISING_SCREEN_ANDROID_SCREEN_LOAD_TIMEOUT = 10
PLATFORM = Configuration.get_instance().platform_type()


class AdvertisingTests(BaseTest):
    def verify_banner(self, step, unit_id, banner_type):
        interstitial_screen = self.building_blocks.screens[INTERSTITIAL_SCREEN]
        PRINT('Step %s: Verify %s banner with id %s' %
              (step, banner_type, unit_id))
        Logger.get_instance().log_assert(
            interstitial_screen.search_for_item_by_id(unit_id, retries=7),
            '%s banner "%s" not is found on the screen' % (
                banner_type, unit_id)
        )
        PRINT('     Step %s.1: %s banner with id %s found successfully on the screen' % (
            step, banner_type, unit_id))

    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_interstitial_once(self):
        interstitial_once_screen = self.building_blocks.screens[INTERSTITIAL_ONCE_SCREEN]
        advertising_screen = self.building_blocks.screens[ADVERTISING_SCREEN]

        PRINT('Step 1: Navigate to "%s" screen' % INTERSTITIAL_ONCE_SCREEN)
        interstitial_once_screen.navigate()

        PRINT('Step 2: Verify that the interstitial screen is presented')
        advertising_screen.verify_interstitial_is_displaying()

        PRINT('Step 3: Close the interstitial')
        advertising_screen.close_interstitial()

        PRINT('Step 4: Verify that we reached the actual screen behind the interstitial')
        interstitial_once_screen.verify_in_screen()
        item_name = 'vod_0'
        PRINT('     Step 4.1: Verify that item "%s" from the data of the screen is displaying' % item_name)
        Logger.get_instance().log_assert(
            interstitial_once_screen.search_for_item_by_text(
                item_name), '"%s" item not found in the screen' % item_name
        )

        PRINT('Step 5: Navigate back, in order to open the "%s" screen once again' %
              INTERSTITIAL_ONCE_SCREEN)
        self.building_blocks.navigation_bar.press_back_button()
        PRINT('     Step 5.1: Navigate again the "%s" screen' %
              INTERSTITIAL_ONCE_SCREEN)
        interstitial_once_screen.navigate()
        PRINT('     Step 5.2: Wait 3 seconds to see if the interstitial did show')
        advertising_screen.verify_interstitial_is_not_displaying()
        PRINT('     Step 5.3: Verify we reached the "%s" screen and that id did load correctly' %
              INTERSTITIAL_ONCE_SCREEN)
        interstitial_once_screen.verify_in_screen()
        item_name = 'vod_0'
        PRINT('     Step 5.4: Verify that item "%s" from the data of the screen is displaying' % item_name)
        Logger.get_instance().log_assert(
            advertising_screen.search_for_item_by_text(
                item_name, retries=3), '"%s" item not found in the screen' % item_name
        )

    # @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_interstitial_and_banners(self):
        PRINT("Test is commented out temporarily")
        # interstitial_screen = self.building_blocks.screens[INTERSTITIAL_SCREEN]
        # advertising_screen = self.building_blocks.screens[ADVERTISING_SCREEN]

        # PRINT('Step 1: Navigate to "%s" screen' % INTERSTITIAL_SCREEN)
        # interstitial_screen.navigate()

        # PRINT('Step 2: Verify that the interstitial screen is presented')
        # advertising_screen.verify_interstitial_is_displaying()

        # PRINT('Step 3: Close the interstitial')
        # advertising_screen.close_interstitial()

        # PRINT('Step 4: Verify that we reached the actual screen behind the interstitial')
        # interstitial_screen.verify_in_screen()
        # if PLATFORM == PlatformType.ANDROID:
        #     PRINT('     Step 4.1: Start waiting for advertising screen to load')
        #     self.driver.wait(ADVERTISING_SCREEN_ANDROID_SCREEN_LOAD_TIMEOUT)
        #     PRINT('     Step 4.2: Finished waiting for advertising screen to load')

        # item_name = 'vod_0'
        # PRINT('     Step 4.1: Verify that item "%s" from the data of the screen is displaying' % item_name)
        # Logger.get_instance().log_assert(
        #     interstitial_screen.search_for_item_by_text(
        #         item_name, retries=5), '"%s" item not found in the screen' % item_name
        # )

        # # self.verify_banner(5, '/19489716/smartbanner_test', 'smart')
        # self.verify_banner(6, '/5644/es.lasestrellas.app/home', 'standard')
        # self.verify_banner(7, '/5644/es.lasestrellas.app/secciones', 'box')

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_verify_interstitial_and_banners':
            return 'test_verify_interstitial_and_banners:\n' \
                '    Verify that the interstitial and banners are presenting when entering a screen\n'

        if test_name == 'test_verify_interstitial_once':
            return 'test_verify_interstitial:\n' \
                '    Verify that the interstitial is presenting when entering a screen only on the first enter\n'

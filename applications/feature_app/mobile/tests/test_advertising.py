
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Logger

"""
Global Defines
"""
SCREEN_NAME = 'AdvertisingScreen'


class AdvertisingTests(BaseTest):
    @pytest.mark.boaz
    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_interstitial(self):
        advertising_screen = self.building_blocks.screens[SCREEN_NAME]

        PRINT('Step 1: Navigate to "%s" screen' % SCREEN_NAME)
        advertising_screen.navigate()

        PRINT('Step 2: Verify that the interstitial screen is presented')
        advertising_screen.verify_interstitial_is_displaying()

        PRINT('Step 3: Close the interstitial')
        advertising_screen.close_interstitial()
        PRINT('     Step 3.1: Verify that we reached the actual screen behind the interstitial')
        advertising_screen.verify_in_screen()
        item_name = 'vod_0'
        PRINT('     Step 3.2: Verify that item "%s" from the data of the screen is displaying' % item_name)
        Logger.get_instance().log_assert(
            advertising_screen.search_for_item_by_text(item_name), '"%s" item not found in the screen' % item_name
        )

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_verify_interstitial':
            return 'test_verify_interstitial:\n' \
               '    Verify that the interstitial is presenting when entering a screen\n'

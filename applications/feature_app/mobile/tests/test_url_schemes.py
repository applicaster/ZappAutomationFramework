
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.utils.print import PRINT
from src.base_test import BaseTest
from src.verifiers.verifier import Verifier

"""
Global Defines
"""
SCREEN_NAME = 'UrlSchemes'


class UrlSchemesTests(BaseTest):

    @pytest.mark.usefixtures('automation_driver')
    def test_verify_url_scheme_to_screen_by_id(self):
        PRINT('Step 1: Navigate to "%s"' % SCREEN_NAME)
        self.building_blocks.screens[SCREEN_NAME].navigate()

        PRINT('Step 2: Press the url scheme item that leads the user to other Horizontal List UIBuilder screen')
        element = self.driver.find_element_by_text('url_scheme_to_screen')
        element.click()

        PRINT('Step 3: Verify we navigated successfully to "HorizontalList" screen')
        self.building_blocks.screens['HorizontalList'].verify_in_screen(retries=20)
        PRINT('     Step 3.1: Verify text elements in "HorizontalList" screen')
        Verifier(self.driver).verify_elements_on_screen_by_text(('m3u8_vod', 'json_feed'), retries=5)

        # PRINT('Step 4: Verify navigation back to "%s"' % SCREEN_NAME)
        # PRINT('     Step 4.1: Press the navigation bar Back button')
        # self.building_blocks.navigation_bar.press_back_button()
        # PRINT('     Step 4.1: Verify we navigated back successfully to "%s" screen' % SCREEN_NAME)
        # self.building_blocks.screens[SCREEN_NAME].verify_in_screen(retries=5)

    def shortDescription(self, test_name) -> str:
        return 'test_verify_url_scheme_to_screen_by_id:\n' \
               '    TestRail C22996 - Verify URL scheme that opens another screen'

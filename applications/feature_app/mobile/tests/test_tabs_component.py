
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.verifiers.verifier import Verifier

"""
Global Defines
"""
FRACTIONAL_TABS_SCREEN = 'FractionalTabs'


class TabsComponentTests(BaseTest):
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_fractional_tabs(self):
        verifier = Verifier(self.driver)
        fractional_tabs_screen = self.building_blocks.screens[FRACTIONAL_TABS_SCREEN]

        PRINT('Step 1: Navigate to "%s" screen via the side menu' % FRACTIONAL_TABS_SCREEN)
        fractional_tabs_screen.navigate()

        PRINT('Step 2: Verify elements in Tab-1')
        verifier.verify_elements_on_screen_by_text(
            ('json_feed', 'm3u8_vod', 'video_feed_with_ima_extension'),
            retries=7
        )

        PRINT('Step 3: Switch to Tab-2 and verify elements of that tab')
        PRINT('     Step 3.1: Switch to Tab-2')
        self.driver.find_element_by_text('Tab-2').click()
        self.driver.wait(2)
        PRINT('     Step 3.2: Verify elements in Tab-2')
        verifier.verify_elements_on_screen_by_text(
            ('json_feed', 'vod_with_play_next', 'future_program_feed'),
            retries=7
        )

        PRINT('Step 4: Switch to Tab-3 and verify elements of that tab')
        PRINT('     Step 4.1: Switch to Tab-3')
        self.driver.find_element_by_text('Tab-3').click()
        self.driver.wait(2)
        PRINT('     Step 4.2: Verify elements in Tab-3')
        verifier.verify_elements_on_screen_by_text(
            ('json_feed', 'vod_with_play_next', '00:00'),
            retries=7
        )

    def shortDescription(self, test_name) -> str:
        return 'test_verify_fractional_tabs:\n' \
               '    Verify that a fractional tab component is displaying on screen and switch between the tabs'

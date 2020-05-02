
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.verifiers.verifier import Verifier

"""
Global Defines
"""
SCREEN_NAME = 'HorizontalList'


class HorizontalListComponentTests(BaseTest):
    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_horizontal_list(self):
        horizontal_list_screen = self.building_blocks.screens[SCREEN_NAME]

        PRINT('Step 1: Navigate to "%s" screen via the side menu' % SCREEN_NAME)
        horizontal_list_screen.navigate()

        texts_to_search = ('json_feed', 'm3u8_vod', 'video_feed_with_ima_extension')
        PRINT('Step 1: Verify that "%s" found in %s screen correctly' % (texts_to_search, SCREEN_NAME))
        verifier = Verifier(self.driver)
        verifier.verify_elements_on_screen_by_text(texts_to_search, retries=7)

    def shortDescription(self, test_name) -> str:
        return 'test_verify_horizontal_list:\n' \
               '    TestRail C22936 - Verify basic functionality of the rails component\n' \
               '    TestRail C22938 - Verify swiping between cells in the grid component\n' \
               '    TestRail C22943 - Verify functionality of connected feature on grid'


import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT


class GridComponentTests(BaseTest):

    @pytest.mark.usefixtures('automation_driver')
    def test_play_vod_item_in_feed_of_feeds_connected_screen(self):
        grid_screen = self.building_blocks.screens['GridScreen']

        PRINT('Step 1: Navigate to "GridScreen" screen')
        grid_screen.navigate()

        grid_screen.dismiss_react_native_yellow_console_box()

    def shortDescription(self) -> str:
        return 'test_play_vod_item_in_feed_of_feeds_connected_screen:\n' \
               '    TestRail C22942 - Verify basic functionality of the grid component\n' \
               '    TestRail C22938 - Verify swiping between cells in the grid component\n' \
               '    TestRail C22943 - Verify functionality of connected feature on grid'

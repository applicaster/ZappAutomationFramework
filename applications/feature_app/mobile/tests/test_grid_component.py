
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT


class GridComponentTests(BaseTest):

    def search_and_press(self, item_name, screen, step_index, step_description, load_timeout):
        step_index = str(step_index)
        PRINT('Step %s: %s' % (step_index, step_description))
        PRINT('     Step %s.1: Start searching for "%s" item' % (step_index, item_name))
        element = screen.search_for_item_by_text(item_name)
        PRINT('     Step %s.2: Click on "%s" item' % (step_index, item_name))
        element.click()

        PRINT('     Step %s.3: Wait %s seconds until that the screen will load' % (step_index, load_timeout))
        self.driver.wait(load_timeout)
        PRINT('     Step %s.4: Finished waiting for the screen to load' % step_index)

    @pytest.mark.usefixtures('automation_driver')
    def test_play_vod_item_in_feed_of_feeds_connected_screen(self):
        grid_screen = self.building_blocks.screens['GridScreen']

        PRINT('Step 1: Navigate to "GridScreen" screen')
        grid_screen.navigate()

        grid_screen.dismiss_react_native_yellow_console_box()

        self.search_and_press(
            'item_0',
            grid_screen,
            2,
            'Press on feed of feed item named "item_0" that will lead us to a connected screen',
            3
        )
        self.search_and_press(
            'item_0',
            grid_screen,
            3,
            'Step 3: Press on a VOD item named "item_0"',
            10
        )

        PRINT('Step 4.0: Verify that the streaming is playing')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()
        PRINT('     Step 4.1: Streaming is playing correctly')

    def shortDescription(self, test_name) -> str:
        return 'test_play_vod_item_in_feed_of_feeds_connected_screen:\n' \
               '    TestRail C22942 - Verify basic functionality of the grid component\n' \
               '    TestRail C22938 - Verify swiping between cells in the grid component\n' \
               '    TestRail C22962 - Verify transition menu icon and back icon\n' \
               '    TestRail C22943 - Verify functionality of connected feature on grid'

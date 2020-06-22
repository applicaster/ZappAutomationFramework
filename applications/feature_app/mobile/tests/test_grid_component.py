
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Configuration
from src.global_defines import PlatformType

"""
Global Defines
"""
PLATFORM = Configuration.get_instance().platform_type()


class GridComponentTests(BaseTest):

    def search_and_press(self, item_name, screen, step_index, step_description, load_timeout):
        step_index = str(step_index)
        PRINT('Step %s: %s' % (step_index, step_description))
        PRINT('     Step %s.1: Start searching for "%s" item' % (step_index, item_name))
        element = screen.search_for_item_by_text(item_name)
        PRINT('     Step %s.2: Click on "%s" item' % (step_index, item_name))
        element.click()

        if load_timeout > 0:
            PRINT('     Step %s.3: Wait %s seconds until that the screen will load' % (step_index, load_timeout))
            self.driver.wait(load_timeout)
            PRINT('     Step %s.4: Finished waiting for the screen to load' % step_index)

    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_play_vod_item_in_feed_of_feeds_connected_screen(self):
        grid_screen = self.building_blocks.screens['GridScreen']
        pre_hook = self.building_blocks.screens['demo_pre_hook']
        platform_type = Configuration.get_instance().platform_type()

        PRINT('Step 1: Navigate to "GridScreen" screen')
        grid_screen.navigate()

        item_name = 'item_0' if platform_type == PlatformType.ANDROID else '000'

        self.search_and_press(
            item_name,
            grid_screen,
            2,
            'Press on feed of feed item named "%s" that will lead us to a connected screen' % item_name,
            3
        )

        item_name = 'child_item_0' if platform_type == PlatformType.ANDROID else 'child_000'
        self.search_and_press(
            item_name,
            grid_screen,
            3,
            'Press on a VOD item with id  "%s"' % item_name,
            1
        )

        if Configuration.get_instance().platform_type() == PlatformType.IOS:
            PRINT('Step 4: Verify that the pre hook screen is presented and dismiss it')
            pre_hook.verify_in_screen(retries=3)
            PRINT('     Step 4.1: Pre hook screen is presented correctly')
            pre_hook.enter_with_success()
            PRINT('     Step 4.2: Pre hook screen dismissed')
            PRINT('     Step 4.3: Wait 10 seconds until the streaming will start')

        PRINT('Wait 10 seconds until that the streaming will start')
        self.driver.wait(10)

        PRINT('Step 5: Verify that the streaming is playing correctly')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()
        PRINT('     Step 5.1: Streaming is playing correctly')

    def shortDescription(self, test_name) -> str:
        return 'test_play_vod_item_in_feed_of_feeds_connected_screen:\n' \
               '    TestRail C22942 - Verify basic functionality of the grid component\n' \
               '    TestRail C22938 - Verify swiping between cells in the grid component\n' \
               '    TestRail C22962 - Verify transition menu icon and back icon\n' \
               '    TestRail C22943 - Verify functionality of connected feature on grid'

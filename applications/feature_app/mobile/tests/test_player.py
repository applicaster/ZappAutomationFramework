
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT

"""
Global Defines
"""
START_PLAYING_VOD_TIMEOUT = 10
SCREEN_NAME = 'ListScreen'


class PlayerTest(BaseTest):

    def find_play_and_verify(self, screen_name, vod_name):
        screen = self.building_blocks.screens[screen_name]

        PRINT('Step 1: Navigate to "%s" screen' % screen_name)
        screen.navigate()

        # TODO: workaround, we need to cancel here the showing of RN yellow debug
        screen.dismiss_react_native_yellow_console_box()

        PRINT('Step 2: Press on vod "%s" item' % vod_name)
        PRINT('     Step 2.1: Search for vod "%s" item on the screen' % vod_name)
        element = screen.search_for_item_by_text(vod_name)
        PRINT('     Step 2.2: Tap on "%s" vod item in order to start playing it' % vod_name)
        element.click()

        PRINT('     Step 2.3: Wait %s seconds until the streaming will start' % START_PLAYING_VOD_TIMEOUT)
        self.driver.wait(START_PLAYING_VOD_TIMEOUT)
        PRINT('     Step 2.4: Finished waiting the %s seconds' % START_PLAYING_VOD_TIMEOUT)

        screen.dismiss_react_native_yellow_console_box()
        self.building_blocks.screens['player_screen'].press_play_pause_button()
        self.building_blocks.screens['player_screen'].verify_stream_is_not_playing()

        self.building_blocks.screens['player_screen'].press_play_pause_button()
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()

    @pytest.mark.boaz
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_json_feed_vod_streaming_in_list_component(self):
        self.find_play_and_verify(SCREEN_NAME, 'm3u8_vod')

    @pytest.mark.usefixtures('automation_driver')
    def test_verify_cms_vod_streaming_in_list_component(self):
        self.find_play_and_verify(SCREEN_NAME, 'vod_0')

    def shortDescription(self, test_name) -> str:
        return 'test_verify_json_feed_vod_streaming_in_list_component:\n' \
               '    TestRail C22957 - Verify playing a VOD from feed\n' \
               '    TestRail C22931 - Verify swiping between cells in the list component\n' \
               '    TestRail C22940 - Verify basic functionality of the list component\n' \
               '\n' \
               'test_verify_cms_vod_streaming_in_list_component:\n' \
               '    TestRail C22958 - Verify playing a VOD from CMS'

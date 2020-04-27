
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT

"""
Global Defines
"""
START_PLAYING_VOD_TIMEOUT = 10


class PlayerTest(BaseTest):

    def find_play_and_verify(self, screen_name, vod_name):
        screen = self.building_blocks.screens[screen_name]

        PRINT('Step 1: Navigate to "%s" screen' % screen_name)
        screen.navigate()

        # TODO: workaround, we need to cancel here the showing of RN yellow debug
        self.driver.find_element_by_text('Dismiss All').click()

        PRINT('Step 2: Press on vod "%s" item' % vod_name)
        PRINT('     Step 2.1: Search for vod "%s" item on the screen' % vod_name)
        element = screen.search_for_item_by_text(vod_name)
        PRINT('     Step 2.2: Tap on "%s" vod item in order to start playing it' % vod_name)
        element.click()

        PRINT('     Step 2.3: Wait %s seconds until the streaming will start' % START_PLAYING_VOD_TIMEOUT)
        self.driver.wait(START_PLAYING_VOD_TIMEOUT)
        PRINT('     Step 2.4: Finished waiting the %s seconds' % START_PLAYING_VOD_TIMEOUT)

        PRINT('Step 3.0: Verify that the streaming is playing')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()
        PRINT('     Step 3.1: Streaming is playing correctly')

    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_json_feed_vod_streaming(self):
        self.find_play_and_verify('ListScreen', 'm3u8_vod')

    @pytest.mark.usefixtures('automation_driver')
    def test_verify_cms_vod_streaming(self):
        self.find_play_and_verify('ListScreen', 'vod_0')

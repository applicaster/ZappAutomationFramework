
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Configuration
from src.global_defines import PlatformType

"""
Global Defines
"""
START_PLAYING_VOD_TIMEOUT = 15
SCREEN_NAME = 'ListScreen'


class PlayerTests(BaseTest):

    def play_item_in_screen(self, screen_name, vod_name):
        screen = self.building_blocks.screens[screen_name]
        pre_hook = self.building_blocks.screens['demo_pre_hook']

        PRINT('Step 1: Navigate to "%s" screen' % screen_name)
        screen.navigate()

        PRINT('Step 2: Press on vod "%s" item' % vod_name)
        PRINT('     Step 2.1: Search for vod "%s" item on the screen' % vod_name)
        element = screen.search_for_item_by_text(vod_name)
        PRINT('     Step 2.2: Tap on "%s" vod item in order to start playing it' % vod_name)
        element.click()
        PRINT('     Step 2.3: Pass the presented pre hook screen with success, in order to watch the video')
        PRINT('     Step 2.4: Verify that the demo pre hook screen is presented')
        pre_hook.verify_in_screen(retries=3)
        PRINT('     Step 2.5: Dismiss the pre hook screen with success')
        pre_hook.enter_with_success()

        PRINT('     Step 2.6: Wait %s seconds until the streaming will start' % START_PLAYING_VOD_TIMEOUT)
        self.driver.wait(START_PLAYING_VOD_TIMEOUT)
        PRINT('     Step 2.7: Finished waiting the %s seconds' % START_PLAYING_VOD_TIMEOUT)

    @pytest.mark.qb_ios_mobile
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_json_feed_vod_streaming_in_list_component(self):
        self.play_item_in_screen(SCREEN_NAME, 'm3u8_vod')

        PRINT('Step 3: Verify that the streaming is playing')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()
        PRINT('     Step 3.1: Streaming is playing correctly')

    @pytest.mark.usefixtures('automation_driver')
    def test_verify_cms_vod_streaming_in_list_component(self):
        self.play_item_in_screen(SCREEN_NAME, 'vod_0')

        PRINT('Step 3: Verify that the streaming is playing')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()
        PRINT('     Step 3.1: Streaming is playing correctly')

    @pytest.mark.usefixtures('automation_driver')
    def test_pause_stream(self):
        screen = self.building_blocks.screens[SCREEN_NAME]
        player_screen = self.building_blocks.screens['player_screen']

        self.play_item_in_screen(SCREEN_NAME, 'm3u8_vod')

        pre_roll_timeout = 20
        PRINT('Step 3: Wait %s seconds until that the pre roll will finish playing' % pre_roll_timeout)
        self.driver.wait(pre_roll_timeout)

        PRINT('Step 4: Pause the stream')
        player_screen.press_pause_button()
        PRINT('     Step 4.1: Verify that the streaming is paused')
        player_screen.verify_stream_is_not_playing()

        PRINT('Step 5: Close player and verify we navigated back to %s screen' % SCREEN_NAME)
        PRINT('     Step 5.1: Close player')
        player_screen.press_close_button()
        PRINT('     Step 5.2: Verify we are in %s screen' % SCREEN_NAME)
        screen.verify_in_screen(retries=15)

    @pytest.mark.usefixtures('automation_driver')
    def test_scrub_progress_bar(self):
        screen = self.building_blocks.screens[SCREEN_NAME]
        player_screen = self.building_blocks.screens['player_screen']

        self.play_item_in_screen(SCREEN_NAME, 'm3u8_vod')

        pre_roll_timeout = 20
        PRINT('Step 3: Wait %s seconds until that the pre roll will finish playing' % pre_roll_timeout)
        self.driver.wait(pre_roll_timeout)

        PRINT('Step 6: Scrub the progress bar to the end')
        player_screen.press_progress_bar(end_offset=15)
        PRINT('     Step 6.1: Verify we navigated back to %s screen' % SCREEN_NAME)
        screen.verify_in_screen(retries=20)

    @pytest.mark.usefixtures('automation_driver')
    def test_ffwd_button(self):
        screen = self.building_blocks.screens[SCREEN_NAME]
        player_screen = self.building_blocks.screens['player_screen']

        self.play_item_in_screen(SCREEN_NAME, 'current_program_feed')

        counter = 5
        PRINT('Step 3: Press the ffwd button %s times' % counter)
        for i in range(counter):
            PRINT('     Step 3.%s: Press on the ffwd button for the %s time' % (i, i+1))
            player_screen.press_ffwd_button()

        screen.verify_in_screen(retries=15)

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_verify_json_feed_vod_streaming_in_list_component':
            return 'test_verify_json_feed_vod_streaming_in_list_component:\n' \
               '    TestRail C22957 - Verify playing a VOD from feed\n' \
               '    TestRail C22931 - Verify swiping between cells in the list component\n' \
               '    TestRail C22940 - Verify basic functionality of the list component\n'

        if test_name == 'test_verify_json_feed_vod_streaming_in_list_component':
            return 'test_verify_cms_vod_streaming_in_list_component:\n' \
                   '    TestRail C22958 - Verify playing a VOD from CMS'

        if test_name == 'test_scrub_progress_bar':
            return 'test_scrub_progress_bar:\n' \
                   '    Scrub the progress bar to the end of the VOD and verify that the player closing to ListScreen'

        if test_name == 'test_pause_stream':
            return 'test_pause_stream:\n' \
                   '    Verify that pause button pausing the stream playing'

        if test_name == 'test_ffwd_button':
            return 'test_ffwd_button:\n' \
                   '    TestRail C22945 - Verify skip forward in video'

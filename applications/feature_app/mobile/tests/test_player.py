
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Configuration
from src.global_defines import PlatformType

"""
Global Defines
"""
START_PLAYING_VOD_TIMEOUT = 15
SCREEN_NAME = 'ListScreen'


class PlayerTest(BaseTest):

    def find_play_and_verify(self, screen_name, vod_name):
        screen = self.building_blocks.screens[screen_name]
        pre_hook = self.building_blocks.screens['demo_pre_hook']

        PRINT('Step 1: Navigate to "%s" screen' % screen_name)
        screen.navigate()

        PRINT('Step 2: Press on vod "%s" item' % vod_name)
        PRINT('     Step 2.1: Search for vod "%s" item on the screen' % vod_name)
        element = screen.search_for_item_by_text(vod_name)
        PRINT('     Step 2.2: Tap on "%s" vod item in order to start playing it' % vod_name)
        element.click()
        if Configuration.get_instance().platform_type() == PlatformType.IOS:
            PRINT('     Step 2.3: Pass the presented pre hook screen with success, in order to watch the video')
            PRINT('     Step 2.4: Verify that the demo pre hook screen is presented')
            pre_hook.verify_in_screen(retries=3)
            PRINT('     Step 2.5: Dismiss the pre hook screen with success')
            pre_hook.enter_with_success()

        PRINT('     Step 2.3: Wait %s seconds until the streaming will start' % START_PLAYING_VOD_TIMEOUT)
        self.driver.wait(START_PLAYING_VOD_TIMEOUT)
        PRINT('     Step 2.4: Finished waiting the %s seconds' % START_PLAYING_VOD_TIMEOUT)

        PRINT('Step 3.0: Verify that the streaming is playing')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()
        PRINT('     Step 3.1: Streaming is playing correctly')

    @pytest.mark.qb_ios_mobile
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_json_feed_vod_streaming_in_list_component(self):
        item_name = 'm3u8_vod' if Configuration.get_instance().platform_type() == PlatformType.ANDROID else 'Id1'
        self.find_play_and_verify(SCREEN_NAME, item_name)

    @pytest.mark.usefixtures('automation_driver')
    def test_verify_cms_vod_streaming_in_list_component(self):
        self.find_play_and_verify(SCREEN_NAME, 'vod_0')

    @pytest.mark.usefixtures('automation_driver')
    def test_pause_stream(self):
        screen = self.building_blocks.screens[SCREEN_NAME]
        pre_hook = self.building_blocks.screens['demo_pre_hook']
        player_screen = self.building_blocks.screens['player_screen']
        vod_name = 'm3u8_vod'

        PRINT('Step 1: Navigate to "%s" screen' % SCREEN_NAME)
        screen.navigate()
        PRINT('Step 2: Press on vod "%s" item' % vod_name)
        PRINT('     Step 2.1: Search for vod "%s" item on the screen' % vod_name)
        element = screen.search_for_item_by_text(vod_name)
        PRINT('     Step 2.2: Tap on "%s" vod item in order to start playing it' % vod_name)
        element.click()
        if Configuration.get_instance().platform_type() == PlatformType.IOS:
            PRINT('     Step 2.3: Pass the presented pre hook screen with success, in order to watch the video')
            PRINT('     Step 2.4: Verify that the demo pre hook screen is presented')
            pre_hook.verify_in_screen(retries=3)
            PRINT('     Step 2.5: Dismiss the pre hook screen with success')
            pre_hook.enter_with_success()

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

    @pytest.mark.boaz
    @pytest.mark.usefixtures('automation_driver')
    def test_scrub_progress_bar(self):
        screen = self.building_blocks.screens[SCREEN_NAME]
        pre_hook = self.building_blocks.screens['demo_pre_hook']
        player_screen = self.building_blocks.screens['player_screen']
        vod_name = 'm3u8_vod'

        PRINT('Step 1: Navigate to "%s" screen' % SCREEN_NAME)
        screen.navigate()
        PRINT('Step 2: Press on vod "%s" item' % vod_name)
        PRINT('     Step 2.1: Search for vod "%s" item on the screen' % vod_name)
        element = screen.search_for_item_by_text(vod_name)
        PRINT('     Step 2.2: Tap on "%s" vod item in order to start playing it' % vod_name)
        element.click()
        if Configuration.get_instance().platform_type() == PlatformType.IOS:
            PRINT('     Step 2.3: Pass the presented pre hook screen with success, in order to watch the video')
            PRINT('     Step 2.4: Verify that the demo pre hook screen is presented')
            pre_hook.verify_in_screen(retries=3)
            PRINT('     Step 2.5: Dismiss the pre hook screen with success')
            pre_hook.enter_with_success()

        pre_roll_timeout = 20
        PRINT('Step 3: Wait %s seconds until that the pre roll will finish playing' % pre_roll_timeout)
        self.driver.wait(pre_roll_timeout)
        player_screen.press_progress_bar(end_offset=10)

    def shortDescription(self, test_name) -> str:
        return 'test_verify_json_feed_vod_streaming_in_list_component:\n' \
               '    TestRail C22957 - Verify playing a VOD from feed\n' \
               '    TestRail C22931 - Verify swiping between cells in the list component\n' \
               '    TestRail C22940 - Verify basic functionality of the list component\n' \
               '\n' \
               'test_verify_cms_vod_streaming_in_list_component:\n' \
               '    TestRail C22958 - Verify playing a VOD from CMS'

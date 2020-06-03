
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.global_defines import RemoteControlKeys


class PlayerTest(BaseTest):
    # @pytest.mark.tv_os
    @pytest.mark.android_tv
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_vod_streaming(self):
        PRINT('Step 1: Start playing "video_feed" vod item from the first component')
        self.driver.send_keys(RemoteControlKeys.ENTER)
        timeout = 10
        PRINT('     Step 1.1: Wait %s seconds until the streaming will start' % timeout)
        self.driver.wait(timeout)

        PRINT('Step 2: Verify streaming is playing correctly')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()
        PRINT('     Step 2.1: Streaming is playing correctly')

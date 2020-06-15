
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Configuration
from src.global_defines import PlatformType
from src.utils.logger import Logger


class GoogleInteractiveMediaAdsTests(BaseTest):
    @pytest.mark.usefixtures('automation_driver')
    @pytest.mark.ima
    def test_verify_playing_vast_ads_from_json_feed(self):
        grid_screen = self.building_blocks.screens['GridScreen']
        pre_hook = self.building_blocks.screens['demo_pre_hook']
        platform_type = Configuration.get_instance().platform_type()

        PRINT('Step 1: Navigate to "GridScreen" screen')
        grid_screen.navigate()

        item_name = 'm3u8_vod' if platform_type == PlatformType.ANDROID else 'Id1'
        PRINT('Step 2: Press on item "%s" element on screen' % item_name)
        element = self.driver.find_element_by_text(item_name)
        element.click()

        PRINT('Step 3: Pass the presented pre hook screen with success, in order to watch the video')
        PRINT('     Step 3.1: Verify that the demo pre hook screen is presented')
        pre_hook.verify_in_screen(retries=3)
        PRINT('     Step 3.2: Dismiss the pre hook screen with success')
        pre_hook.enter_with_success()

        PRINT('Step 4: Verify that a VAST pre-roll adv is presented before the video start playing')
        pre_roll_unit_id = \
            'https://pubads.g.doubleclick.net/gampad/ads?sz=640x480&iu=/124319096/external/single_ad_samples&ciu_szs=300x250&impl=s&gdfp_req=1&env=vp&output=vast&unviewed_position_start=1&cust_params=deployment%3Ddevsite%26sample_ct%3Dredirectlinear&correlator='
        element = self.driver.find_element_by_text(pre_roll_unit_id, 20)
        Logger.get_instance().log_assert(element, 'Test failed displaying video pre roll adv with id: "%s"' % pre_roll_unit_id)
        PRINT('Test verified successfully pre-roll video adv with id "%s"' % pre_roll_unit_id)

        PRINT('Step 5: Verify that the pre-roll completes playing and that the video starts instead')
        timeout = 15
        PRINT('     Step 5.1: Wait %s seconds until the pre-roll will complete' % timeout)
        self.driver.wait(15)
        PRINT('     Step 5.2: Verify that the expected video is playing the streaming correctly')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()

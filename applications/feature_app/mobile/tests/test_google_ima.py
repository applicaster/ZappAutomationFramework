
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Configuration
from src.global_defines import PlatformType
from src.utils.logger import Logger


"""
Global Defines
"""
VMAP_PRE_ROLL_URL = 'https://pubads.g.doubleclick.net/gampad/ads?slotname=/124319096/external/ad_rule_samples&sz=' \
                    '640x480&ciu_szs=300x250&cust_params=deployment%3Ddevsite%26sample_ar%3Dpremidpost&url=&unvie' \
                    'wed_position_start=1&output=xml_vast3&impl=s&env=vp&gdfp_req=1&ad_rule=0&vad_type=linear&vpo' \
                    's=preroll&pod=1&ppos=1&lip=true&min_ad_duration=0&max_ad_duration=30000&vrid=6256&video_doc_' \
                    'id=short_onecue&cmsid=496&kfa=0&tfcd=0'

VMAP_MID_ROLL_URL = 'https://pubads.g.doubleclick.net/gampad/ads?slotname=/124319096/external/ad_rule_samples&sz=' \
                    '640x480&ciu_szs=300x250&cust_params=deployment%3Ddevsite%26sample_ar%3Dpremidpost&url=&unvie' \
                    'wed_position_start=1&output=xml_vast3&impl=s&env=vp&gdfp_req=1&ad_rule=0&cue=15000&vad_type=' \
                    'linear&vpos=midroll&pod=2&mridx=1&rmridx=1&ppos=1&lip=true&min_ad_duration=0&max_ad_duration' \
                    '=30000&vrid=6256&video_doc_id=short_onecue&cmsid=496&kfa=0&tfcd=0'

VMAP_POST_ROLL_URL = 'https://pubads.g.doubleclick.net/gampad/ads?slotname=/124319096/external/ad_rule_samples&sz' \
                     '=640x480&ciu_szs=300x250&cust_params=deployment%3Ddevsite%26sample_ar%3Dpremidpost&url=&unv' \
                     'iewed_position_start=1&output=xml_vast3&impl=s&env=vp&gdfp_req=1&ad_rule=0&vad_type=linear&' \
                     'vpos=postroll&pod=3&ppos=1&lip=true&min_ad_duration=0&max_ad_duration=30000&vrid=6256&video' \
                     '_doc_id=short_onecue&cmsid=496&kfa=0&tfcd=0'

VMAP_VOD_ITEM_NAME = 'vod_with_play_next' if Configuration.get_instance().platform_type() == PlatformType.ANDROID else 'Id2'
VAST_VOD_ITEM_NAME = 'm3u8_vod' if Configuration.get_instance().platform_type() == PlatformType.ANDROID else 'Id1'
VMAP_ADV_URL = 'https://assets-secure.applicaster.com/qa/zapp_qa/automation/advertising/pre_mid_post_roll_vmap.xml'


class GoogleInteractiveMediaAdsTests(BaseTest):
    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_playing_vast_adv_from_json_feed(self):
        grid_screen = self.building_blocks.screens['GridScreen']
        pre_hook = self.building_blocks.screens['demo_pre_hook']

        PRINT('Step 1: Navigate to "GridScreen" screen')
        grid_screen.navigate()

        PRINT('Step 2: Press on item "%s" element on screen' % VAST_VOD_ITEM_NAME)
        element = self.driver.find_element_by_text(VAST_VOD_ITEM_NAME)
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
        PRINT('     Step 5.1: Wait %s seconds until the pre-roll will complete playing the adv' % timeout)
        self.driver.wait(15)
        element = self.driver.find_element_by_text(pre_roll_unit_id)
        Logger.get_instance().log_assert(element is None, 'pre-roll dismissed from screen successfully')
        PRINT('     Step 5.2: Pre-roll dismissed from screen successfully')
        PRINT('     Step 5.3: Verify that the expected video is playing the streaming correctly')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()

    def wait_until_adv_is_gone(self, unit_id, timeout=20):
        for i in range(timeout):
            element = self.driver.find_element_by_text(unit_id)
            if element is None:
                return True
            self.driver.wait(1)
        return False

    def verify_adv(self, step, section, display_timeout, dismiss_timeout, expected_unit_id):
        step = str(step)
        PRINT('Step %s: Verify playing of VMAP %s with id %s' % (step, section, expected_unit_id))
        element = self.driver.find_element_by_text(VMAP_ADV_URL, display_timeout)
        Logger.get_instance().log_assert(element, 'Test failed displaying VMAP %s with id %s' % (section, expected_unit_id))
        PRINT('     Step %s.2: Wait for the %s to complete' % (step, section))
        is_gone = self.wait_until_adv_is_gone(VMAP_ADV_URL, dismiss_timeout)
        Logger.get_instance().log_assert(is_gone, '%s did not dismiss after %s' % (section, dismiss_timeout))
        PRINT('     Step %s.3: %s adv displayed and dismissed successfully' % (step, section))

    @pytest.mark.usefixtures('automation_driver')
    def test_verify_playing_vmap_adv_from_ui_builder_fallback(self):
        grid_screen = self.building_blocks.screens['GridScreen']
        pre_hook = self.building_blocks.screens['demo_pre_hook']

        PRINT('Step 1: Navigate to "GridScreen" screen')
        grid_screen.navigate()

        PRINT('Step 2: Press on item "%s" element on screen' % VMAP_VOD_ITEM_NAME)
        element = self.driver.find_element_by_text(VMAP_VOD_ITEM_NAME)
        element.click()
        PRINT('     Step 2.1: Wait for pre hook and dismiss it')
        self.driver.wait(2)
        pre_hook.enter_with_success()

        self.verify_adv(3, 'pre-roll', 20, 15, VMAP_PRE_ROLL_URL)
        self.verify_adv(4, 'mid-roll', 30, 15, VMAP_MID_ROLL_URL)
        self.verify_adv(5, 'post-roll', 30, 15, VMAP_POST_ROLL_URL)

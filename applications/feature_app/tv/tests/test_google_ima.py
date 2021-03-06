
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT, Configuration
from src.global_defines import PlatformType, RemoteControlKeys
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

VMAP_ADV_URL = 'https://assets-secure.applicaster.com/qa/zapp_qa/automation/advertising/pre_mid_post_roll_vmap.xml'

VMAP_VOD_ITEM_NAME = 'current_program_feed'
VAST_VOD_ITEM_NAME = '002'

PLATFORM = Configuration.get_instance().platform_type()


class GoogleInteractiveMediaAdsTests(BaseTest):
    @pytest.mark.tv_os_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_playing_vast_adv_from_json_feed(self):
        PRINT('Step 1: Play item with VAST adv: %s' % VAST_VOD_ITEM_NAME)
        self.driver.send_keys(RemoteControlKeys.ENTER, 2)

        PRINT('Step 2: Verify that a VAST pre-roll adv is presented before that the video start playing')
        pre_roll_unit_id = \
            'https://pubads.g.doubleclick.net/pcs/click?xai=AKAOjssEaTazxUzioRp_opiQvL6ll0nxp7L6BFR21Rbl5u7N3ekgqQEx12OLsjZPcCgrfAJcTgFj6GQIOO2wd0Iet7LNxsPiiVL-rTBKpdYKu9mT8JmZCLiGGfz1L9DCSO9SsQcsVgJ9CEuGJ7TpO2a0XREwrvxPmWC8x5Jo-cDAwJvkcMeb_9lmBAKk7IhXr8VUyo3zwqUTgtI3s2WXGo73N92DAiqBfEHJhUyr_83p0veAhPE7v4AY1itOhZ0Lgc__u2-_61VZESybCCTpk_uViDMB4pzkTg&sai=AMfl-YQnEMttDV5oCIaH_X_MEeQACtNInh2lo6uiaGK7cuCHY3yu-S4hwe2Db5y4hdMvVDgY0AtdSyhTLvoTcEhNYP5bi3VXkZmkA3_kttEhybvSrwk8JgS48xkmHsAsnIOlVM3on4eddexfSsD-gj88ZnijleNgB5OaRoyb&sig=Cg0ArKJSzGfhhZLS4nJ6&adurl=https://developers.google.com/interactive-media-ads/docs/vastinspector_dual'
        if PLATFORM == PlatformType.TV_OS:
            pre_roll_unit_id = \
            'https://pubads.g.doubleclick.net/gampad/ads?sz=640x480&iu=/124319096/external/single_ad_samples&ciu_szs=300x250&impl=s&gdfp_req=1&env=vp&output=vast&unviewed_position_start=1&cust_params=deployment%3Ddevsite%26sample_ct%3Dredirectlinear&correlator='

        element = self.driver.find_element_by_text(pre_roll_unit_id, 20)
        Logger.get_instance().log_assert(
            element,
            'Test failed displaying video pre roll adv with id: "%s"' % pre_roll_unit_id
        )
        PRINT('Test verified successfully pre-roll video adv with id "%s"' % pre_roll_unit_id)

        PRINT('Step 5: Verify that the pre-roll completes playing and that the video starts instead')
        timeout = 15
        PRINT('     Step 5.1: Wait %s seconds until the pre-roll will complete playing the adv' % timeout)
        self.driver.wait(timeout)
        element = self.driver.find_element_by_text(pre_roll_unit_id)
        Logger.get_instance().log_assert(element is None, 'pre-roll did not dismiss from screen')
        PRINT('     Step 5.2: Pre-roll has dismissed from screen successfully')
        PRINT('     Step 5.3: Verify that the expected video is playing the streaming correctly')
        self.building_blocks.screens['player_screen'].verify_stream_is_playing()

    def wait_until_adv_is_gone(self, unit_id, timeout=20):
        for i in range(timeout):
            element = self.driver.find_element_by_accessibility_id(unit_id)
            if element is None:
                return True
            self.driver.wait(1)
        return False

    def verify_adv(self, step, section, display_timeout, dismiss_timeout, expected_unit_id):
        step = str(step)
        PRINT('Step %s: Verify playing of VMAP %s with id %s' % (step, section, expected_unit_id))
        element = self.driver.find_element_by_accessibility_id(VMAP_ADV_URL, display_timeout)

        Logger.get_instance().log_assert(element, 'Test failed displaying VMAP %s with id %s' % (section, expected_unit_id))
        PRINT('     Step %s.2: Wait for the %s to complete' % (step, section))
        is_gone = self.wait_until_adv_is_gone(VMAP_ADV_URL, dismiss_timeout)
        Logger.get_instance().log_assert(is_gone, '%s did not dismiss after %s' % (section, dismiss_timeout))
        PRINT('     Step %s.3: %s adv displayed and dismissed successfully' % (step, section))

    @pytest.mark.tv_os_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_playing_vmap_adv_from_ui_builder_fallback(self):
        PRINT('Step 1: Play item with UIBuilder VMAP fallback adv: %s' % VMAP_VOD_ITEM_NAME)
        self.driver.send_keys([RemoteControlKeys.RIGHT, RemoteControlKeys.ENTER], 2)

        self.verify_adv(3, 'pre-roll', 20, 15, VMAP_PRE_ROLL_URL)
        self.verify_adv(4, 'mid-roll', 30, 15, VMAP_MID_ROLL_URL)
        self.verify_adv(5, 'post-roll', 45, 15, VMAP_POST_ROLL_URL)

        PRINT('Step 3: Verify that the app navigated back to Home after playing the post roll')
        self.building_blocks.screens['Home'].verify_in_screen(retries=10)

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_verify_playing_vast_adv_from_json_feed':
            return 'Verify playing of pre roll from a json feed VOD item extension'

        if test_name == 'test_verify_playing_vmap_adv_from_ui_builder_fallback':
            return 'Verify playing of pre/mid/post roll VMPA ad url that is defined as fall back ad url in the plugin' \
                   ' configuration'

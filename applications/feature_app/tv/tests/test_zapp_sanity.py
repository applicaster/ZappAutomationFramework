
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.configuration.configuration import Configuration
from src.global_defines import PlatformType
from src.global_defines import RemoteControlKeys
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.base_test import BaseTest


@pytest.mark.tv_os_nightly
@pytest.mark.samsung_tv_nightly
@pytest.mark.tv_os
@pytest.mark.usefixtures('automation_driver')
class SimpleLaunchToHomeScreenTest(BaseTest):
    def verify_text_on_screen(self, text):
        element = self.driver.find_element_by_text(text, 5)
        Logger.get_instance().log_assert(element, 'Test failed to find "%s" text on screen' % text)
        PRINT('"%s" title found on screen correctly' % text)

    def test_launch_to_home_screen(self):
        PRINT('Step 1: Verify that the TV top menu bar items showing correctly on screen')
        self.building_blocks.screens['Home'].verify_in_screen()
        self.verify_text_on_screen('Home')
        self.verify_text_on_screen('Hero Screen')
        self.verify_text_on_screen('Screen Picker')
        self.verify_text_on_screen('Mixed Screen')


def verify_component(driver, step_num, step_title, items):
    PRINT(step_title)
    counter = 0
    for item in items:
        counter += 1
        element = driver.find_element_by_text(item, retries=7)
        Logger.get_instance().log_assert(element, 'Test failed to find "%s" on screen' % item)
        PRINT('     Step %s.%s: Item %s found on screen' % (str(step_num), str(counter), item))


@pytest.mark.android_tv
@pytest.mark.samsung_tv
@pytest.mark.usefixtures('automation_driver')
class GridScreenTest(BaseTest):
    def test_grid_screen(self):
        platform = Configuration.get_instance().platform_type()

        PRINT('Step 1: Verify that the application launched in home screen')
        self.building_blocks.screens['Home'].verify_in_screen()

        verify_component(
            self.driver,
            2,
            'Step 2: Verify json feed data in Grid component',
            ['applicaster_cell_types', 'video_feed', 'current_program_feed', 'channel_feed']
        )

        if platform in [PlatformType.ANDROID_TV]:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            3,
            'Step 3: Verify XML feed data in Grid component',
            ['video_feed_xml_mp4_and_m3u8', 'vod_mp4_item_1', 'vod_mp4_item_2', 'vod_mp4_item_3', 'vod_mp4_item_2']
        )

        if platform in [PlatformType.ANDROID_TV]:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            3,
            'Step 3.1: Verify XML feed data in Grid component',
            ['vod_m3u8_item_1', 'vod_m3u8_item_2', 'vod_m3u8_item_3', 'vod_m3u8_item_4']
        )

        if platform in [PlatformType.ANDROID_TV]:
            self.driver.send_keys([RemoteControlKeys.DOWN, RemoteControlKeys.DOWN, RemoteControlKeys.DOWN], 3)
        verify_component(
            self.driver,
            4,
            'Step 4: Verify Applicaster 2 category in Grid component',
            ['vod_0', 'vod_1', 'vod_2', 'vod_3']
        )

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_grid_screen':
            return 'test_grid_screen:' \
                   'TestRail C10293 - Verify basic functionality of grid component' \
                   'TestRail C10280	- Verify Grid is displaying correct with different datasources'


@pytest.mark.samsung_tv
@pytest.mark.usefixtures('automation_driver')
class HorizontalListScreenTest(BaseTest):
    def test_horizontal_list_screen(self):
        platform_type = Configuration.get_instance().platform_type()

        PRINT('Step 1: Verify that the application launched into home screen')
        self.building_blocks.screens['Home'].verify_in_screen()

        PRINT('Step 2: navigate to "Horizontal List Screen" screen from top menu bar')
        self.building_blocks.screens['Horizontal List Screen'].navigate()

        verify_component(
            self.driver,
            3,
            'Step 1: Verify xml feed data in Horizontal List component',
            ['video_feed_xml_mp4_and_m3u8', 'vod_mp4_item_1', 'vod_mp4_item_2', 'vod_mp4_item_3', 'vod_mp4_item_4']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys([RemoteControlKeys.DOWN, RemoteControlKeys.DOWN], 3)
        verify_component(
            self.driver,
            4,
            'Step 2: Verify json feed data in Horizontal List component',
            ['applicaster_cell_types', 'video_feed', 'current_program_feed', 'channel_feed']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys([RemoteControlKeys.DOWN], 3)
        verify_component(
            self.driver,
            5,
            'Step 3: Verify Applicaster 2 category in Horizontal List component',
            ['Samsung TV Category', 'vod_1', 'vod_2', 'vod_3']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys([RemoteControlKeys.DOWN], 3)
        verify_component(
            self.driver,
            6,
            'Step 4: Verify Applicaster 2 collection in Horizontal List component',
            ['Samsung TV Collection', 'vod_0', 'vod_1', 'vod_2', 'vod_3']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            7,
            'Step 5: Verify "damaged data" json feed in Horizontal List component',
            [
                'damaged_atom_feed', 'Correct Item', 'Missing Item Image', 'Damaged Video Url', 'Example summary',
                'Example Image Gallery Title #1', 'Example Program #1'
            ]
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys([RemoteControlKeys.DOWN, RemoteControlKeys.DOWN], 3)
        verify_component(
            self.driver,
            8,
            'Step 6: Verify "big_data_atom_xml" XML feed in Horizontal List component',
            ['big_data_atom_json']
        )


@pytest.mark.android_tv_nightly
@pytest.mark.samsung_tv
@pytest.mark.usefixtures('automation_driver')
class HeroScreenTest(BaseTest):
    def test_hero_screen(self):
        platform_type = Configuration.get_instance().platform_type()

        PRINT('Step 1: navigate to "Hero Screen" screen from top menu bar')
        self.building_blocks.screens['Hero Screen'].navigate()

        verify_component(
            self.driver,
            2,
            'Step 1: Verify xml feed data in Hero component',
            ['video_feed_xml_mp4_and_m3u8', 'vod_mp4_item_1', 'vod_mp4_item_2']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            3,
            'Step 2: Verify json feed data in Hero component',
            ['applicaster_cell_types', 'video_feed', 'current_program_feed', 'channel_feed']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            4,
            'Step 3: Verify Applicaster 2 category in Hero component',
            ['Samsung TV Category', 'vod_1', 'vod_2', 'vod_3']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            5,
            'Step 4: Verify Applicaster 2 collection in Hero component',
            ['Samsung TV Collection']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            6,
            'Step 5: Verify "damaged data" json feed in Hero component',
            ['damaged_atom_feed', 'Correct Item', 'Missing Item Image', 'Damaged Video Url']
        )

        if platform_type == PlatformType.ANDROID_TV:
            self.driver.send_keys(RemoteControlKeys.DOWN, 3)
        verify_component(
            self.driver,
            7,
            'Step 6: Verify "big_data_atom_xml" XML feed in Hero component',
            ['big_data_atom_json']
        )


@pytest.mark.android_tv_nightly
@pytest.mark.samsung_tv
@pytest.mark.usefixtures('automation_driver')
class ScreenPickerScreenTest(BaseTest):
    def test_screen_picker(self):
        platform_type = Configuration.get_instance().platform_type()
        PRINT('Step 1: navigate to "Screen Picker" screen from top menu bar')
        self.building_blocks.screens['Screen Picker'].navigate()

        verify_component(
            self.driver,
            2,
            'Step 2: verify that the screen picker tabs texts are showing on screen',
            ['screen_1', 'screen_2', 'screen_3', 'screen_4', 'applicaster_cell_types', 'video_feed', 'current_program_feed']
        )

        PRINT('Step 3: move to the screen picker tab named "screen_2"')
        self.driver.send_keys([RemoteControlKeys.DOWN, RemoteControlKeys.DOWN, RemoteControlKeys.ENTER])
        self.driver.wait(2)

        elements_to_verify = ['video_feed_xml_mp4_and_m3u8', 'vod_mp4_item_1', 'vod_mp4_item_2', 'vod_mp4_item_3', 'vod_mp4_item_4']
        if platform_type in [PlatformType.ANDROID_TV, PlatformType.TV_OS]:
            self.driver.wait(3)
            elements_to_verify = ['video_feed_xml_mp4_and_m3u8', 'vod_mp4_item_1', 'vod_mp4_item_2']

        verify_component(
            self.driver,
            4,
            'Step 4: verify that the screen picker tab "screen_2" data is showing on screen',
            elements_to_verify
        )

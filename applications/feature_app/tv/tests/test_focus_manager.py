
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.global_defines import RemoteControlKeys
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.base_test import BaseTest


def move_focus_and_verify(driver, step_num, step_description, keys_steps, accessibility_id):
    PRINT('Step %s: %s' % (step_num, step_description))
    driver.send_keys(keys_steps, 1.5)

    is_focused = driver.is_element_focused(accessibility_id)
    Logger.get_instance().log_assert(is_focused is True,
                                     '%s is not focused' % accessibility_id)
    PRINT('     Step %s.2: item "%s" is focused on the screen correctly' %
          (step_num, accessibility_id))


class FocusManagerTests(BaseTest):
    @pytest.mark.usefixtures('automation_driver')
    @pytest.mark.samsung_tv
    def test_move_focus_manager_in_grid_screen(self):
        PRINT('Step 1: Verify that application launched into home screen')
        self.building_blocks.screens['Home'].verify_in_screen()

        accessibility_id = 'focusable-0657822b-4a2f-4524-81da-0f10db13a5e0-001-0'
        move_focus_and_verify(
            self.driver,
            2,
            'verify that on app launch the "vod_m3u8_item_2" in grid component "video_feed_xml_mp4_and_m3u8" is in focus',
            None,
            accessibility_id
        )

        accessibility_id = 'focusable-6a4efb70-dd35-4d25-9e4f-016f9614d1c7-108785-9'
        move_focus_and_verify(
            self.driver,
            3,
            'move focus manager to the bottom item (vod_m3u8_item_6) of the second grid component (video_feed_xml_mp4_and_m3u8)',
            [RemoteControlKeys.DOWN, RemoteControlKeys.DOWN,
                RemoteControlKeys.DOWN, RemoteControlKeys.RIGHT],
            accessibility_id
        )

        accessibility_id = 'focusable-9eda317d-20fc-4db9-9477-f5af17f95ad9-7125723-0'
        move_focus_and_verify(
            self.driver,
            4,
            'move focus manager to the first item (vod_3) of the third grid component (Samsung TV Category)',
            RemoteControlKeys.DOWN,
            accessibility_id
        )

        accessibility_id = 'focusable-6a4efb70-dd35-4d25-9e4f-016f9614d1c7-108785-9'
        move_focus_and_verify(
            self.driver,
            5,
            'move focus manager back to the second grid component, focus item should be vod_m3u8_item_6',
            RemoteControlKeys.UP,
            accessibility_id
        )

    @pytest.mark.samsung_tv
    @pytest.mark.usefixtures('automation_driver')
    def test_move_focus_manager_in_horizontal_list_screen(self):
        PRINT('Step 1: Verify that application launched into home screen')
        self.building_blocks.screens['Home'].verify_in_screen()

        PRINT('Step 2: navigate to "Horizontal List" screen from top menu bar')
        self.building_blocks.screens['Horizontal List Screen'].navigate()

        accessibility_id = 'focusable-9935e5f9-c0f7-48a7-8f22-2a13c28c4acf-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            3,
            'verify if top most left item in top horizontal list component is focused when screen opens (vod_mp4_item_1)',
            None,
            accessibility_id
        )

        accessibility_id = 'focusable-9935e5f9-c0f7-48a7-8f22-2a13c28c4acf-a0276e224d8b7fd8d4250f182033ee8e-1'
        move_focus_and_verify(
            self.driver,
            4,
            'move focus manager to the second item in the first horizontal list component and verify that it is focused (vod_mp4_item_2)',
            RemoteControlKeys.RIGHT,
            accessibility_id
        )

        accessibility_id = 'focusable-fdb69052-ec37-4a12-a030-ba810bfe6a4c-001-0'
        move_focus_and_verify(
            self.driver,
            5,
            'move focus manager to the second horizontal list on screen named "applicaster_cell_types" and verify if '
            'most left item in the second horizontal list is focused (video_feed)',
            RemoteControlKeys.DOWN,
            accessibility_id
        )

        accessibility_id = 'focusable-fdb69052-ec37-4a12-a030-ba810bfe6a4c-002-1'
        move_focus_and_verify(
            self.driver,
            6,
            'move focus manager to the second item in the second horizontal list on screen named "applicaster_cell_types"'
            'verify if the second item in the second horizontal list in screen is focused (current_program_feed)',
            RemoteControlKeys.RIGHT,
            accessibility_id
        )

        accessibility_id = 'focusable-9935e5f9-c0f7-48a7-8f22-2a13c28c4acf-a0276e224d8b7fd8d4250f182033ee8e-1'
        move_focus_and_verify(
            self.driver,
            7,
            'move focus manager back again to the first horizontal list named "video_feed_xml_mp4_and_m3u8"'
            'verify if the second item in the first horizontal list in screen is focused',
            RemoteControlKeys.UP,
            accessibility_id
        )

    @pytest.mark.samsung_tv
    @pytest.mark.usefixtures('automation_driver')
    def test_move_focus_manager_in_hero_screen(self):
        PRINT('Step 1: verify that application launched into home screen')
        self.building_blocks.screens['Home'].verify_in_screen()

        PRINT('Step 2: navigate to "Hero Screen" screen from top menu bar')
        self.building_blocks.screens['Hero Screen'].navigate()

        accessibility_id = 'focusable-bb5dd00a-cd10-483c-8c84-3976d95c97eb-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            3,
            'verify that when hero screen opens the focus item is "vod_mp4_item_1" in hero component "video_feed_xml_mp4_and_m3u8"',
            None,
            accessibility_id
        )

        accessibility_id = 'focusable-bb5dd00a-cd10-483c-8c84-3976d95c97eb-108785-9'
        move_focus_and_verify(
            self.driver,
            4,
            'verify that when moving the focus 1 time to left the focus item is "vod_m3u8_item_6" in hero component "video_feed_xml_mp4_and_m3u8"',
            RemoteControlKeys.LEFT,
            accessibility_id
        )

        accessibility_id = 'focusable-bb5dd00a-cd10-483c-8c84-3976d95c97eb-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            5,
            'verify that when looping the hero from left to the first item the focus manager really focusing vod_mp4_item_1',
            [RemoteControlKeys.LEFT, RemoteControlKeys.LEFT, RemoteControlKeys.LEFT, RemoteControlKeys.LEFT,
             RemoteControlKeys.LEFT, RemoteControlKeys.LEFT, RemoteControlKeys.LEFT, RemoteControlKeys.LEFT, RemoteControlKeys.LEFT],
            accessibility_id
        )

    @pytest.mark.samsung_tv
    @pytest.mark.usefixtures('automation_driver')
    def test_move_focus_manager_in_screen_picker(self):
        PRINT('Step 1: verify that application launched into home screen')
        self.building_blocks.screens['Home'].verify_in_screen()

        PRINT('Step 2: navigate to "Screen Picker Screen" screen from top menu bar')
        self.building_blocks.screens['Screen Picker'].navigate()

        PRINT('Step 3: verify that the first item in the left menu is focused when screen picker screen opens and after 1 press down')
        accessibility_id = 'focusable-437d59bd-985a-4f74-8534-ac8d7981166d.ScreenSelector-58032-0'
        is_focused = self.driver.is_element_focused(accessibility_id)
        Logger.get_instance().log_assert(is_focused is True,
                                         '%s is not focused' % accessibility_id)

        accessibility_id = 'focusable-0657822b-4a2f-4524-81da-0f10db13a5e0-001-0'
        move_focus_and_verify(
            self.driver,
            4,
            'move focus manager from the first item in menu to the picker component and verify that "video_feed" '
            'item is focused',
            RemoteControlKeys.RIGHT,
            accessibility_id
        )

        accessibility_id = 'focusable-6a4efb70-dd35-4d25-9e4f-016f9614d1c7-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            5,
            'move focus manager inside the screen picker grid component and verify that "channel_feed" '
            'becoming focused',
            RemoteControlKeys.DOWN,
            accessibility_id
        )

        accessibility_id = 'focusable-437d59bd-985a-4f74-8534-ac8d7981166d.ScreenSelector-58033-1'
        move_focus_and_verify(
            self.driver,
            6,
            'move focus manger to the second tab in the screen picker (screen_2) and verify that screen_2 is focused',
            [RemoteControlKeys.LEFT,
                RemoteControlKeys.DOWN, RemoteControlKeys.ENTER],
            accessibility_id
        )

    @pytest.mark.samsung_tv
    @pytest.mark.usefixtures('automation_driver')
    def test_move_focus_manager_in_top_menu_bar(self):
        accessibility_id = 'focusable-9935e5f9-c0f7-48a7-8f22-2a13c28c4acf-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            1,
            'navigate from top menu bar to "Horizontal List Screen" and verify focus is on "vod_mp4_item_1" item '
            'in "vod_mp4_item_1" Horizontal List component',
            [RemoteControlKeys.UP, RemoteControlKeys.RIGHT,
                RemoteControlKeys.ENTER],
            accessibility_id
        )

        accessibility_id = 'focusable-bb5dd00a-cd10-483c-8c84-3976d95c97eb-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            2,
            'navigate from top menu bar to "Hero Screen" and verify focus is on "vod_mp4_item_1" item '
            'in "vod_mp4_item_1" Hero component',
            [RemoteControlKeys.UP, RemoteControlKeys.RIGHT,
                RemoteControlKeys.ENTER, RemoteControlKeys.DOWN],
            accessibility_id
        )


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
        self.driver.send_keys(
            [RemoteControlKeys.UP, RemoteControlKeys.DOWN], 1)

        accessibility_id = 'focusable-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-001-0'
        move_focus_and_verify(
            self.driver,
            2,
            'verify that on app launch the "video_feed" in grid component "applicaster_cell_types_json" is in focus',
            None,
            accessibility_id
        )

        accessibility_id = 'focusable-ba9d4f36-1d4c-4cbe-9b6c-9ab457100af5-b2b7c964-fbe6-41b0-aba7-0499653a2ef8-3-1-ba9d4f36-1d4c-4cbe-9b6c-9ab457100af5-b2b7c964-fbe6-41b0-aba7-0499653a2ef8-3-1-108785-9'
        move_focus_and_verify(
            self.driver,
            3,
            'move focus manager to the bottom item (vod_m3u8_item_6) of the second grid component (video_feed_xml_mp4_and_m3u8)',
            [RemoteControlKeys.DOWN, RemoteControlKeys.DOWN,
                RemoteControlKeys.DOWN, RemoteControlKeys.RIGHT],
            accessibility_id
        )

        accessibility_id = 'focusable-501c665a-c663-4631-8ff5-7bbde3cfe209-0716203a-530e-4bfa-925d-441655ca277e-10-1-501c665a-c663-4631-8ff5-7bbde3cfe209-0716203a-530e-4bfa-925d-441655ca277e-10-1-7125723-0'
        move_focus_and_verify(
            self.driver,
            4,
            'move focus manager to the first item (vod_3) of the third grid component (Samsung TV Category)',
            RemoteControlKeys.DOWN,
            accessibility_id
        )

        accessibility_id = 'focusable-ba9d4f36-1d4c-4cbe-9b6c-9ab457100af5-b2b7c964-fbe6-41b0-aba7-0499653a2ef8-3-1-ba9d4f36-1d4c-4cbe-9b6c-9ab457100af5-b2b7c964-fbe6-41b0-aba7-0499653a2ef8-3-1-108785-9'
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
        self.driver.send_keys(RemoteControlKeys.UP)
        self.building_blocks.screens['Horizontal List Screen'].navigate()
        self.driver.send_keys([RemoteControlKeys.UP, RemoteControlKeys.DOWN])

        accessibility_id = 'focusable-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            3,
            'verify if top most left item in top horizontal list component is focused when screen opens (vod_mp4_item_1)',
            None,
            accessibility_id
        )

        accessibility_id = 'focusable-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a0276e224d8b7fd8d4250f182033ee8e-1'
        move_focus_and_verify(
            self.driver,
            4,
            'move focus manager to the second item in the first horizontal list component and verify that it is focused (vod_mp4_item_2)',
            RemoteControlKeys.RIGHT,
            accessibility_id
        )

        accessibility_id = 'focusable-991d5165-8a8e-4f64-930a-6deeb555c2a0-790ba203-3c34-4faa-a395-e3165800e1a0-7-1-991d5165-8a8e-4f64-930a-6deeb555c2a0-790ba203-3c34-4faa-a395-e3165800e1a0-7-1-001-0'
        move_focus_and_verify(
            self.driver,
            5,
            'move focus manager to the second horizontal list on screen named "applicaster_cell_types" and verify if '
            'most left item in the second horizontal list is focused (video_feed)',
            RemoteControlKeys.DOWN,
            accessibility_id
        )

        accessibility_id = 'focusable-991d5165-8a8e-4f64-930a-6deeb555c2a0-790ba203-3c34-4faa-a395-e3165800e1a0-7-1-991d5165-8a8e-4f64-930a-6deeb555c2a0-790ba203-3c34-4faa-a395-e3165800e1a0-7-1-002-1'
        move_focus_and_verify(
            self.driver,
            6,
            'move focus manager to the second item in the second horizontal list on screen named "applicaster_cell_types"'
            'verify if the second item in the second horizontal list in screen is focused (current_program_feed)',
            RemoteControlKeys.RIGHT,
            accessibility_id
        )

        accessibility_id = 'focusable-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a0276e224d8b7fd8d4250f182033ee8e-1'
        move_focus_and_verify(
            self.driver,
            7,
            'move focus manager back again to the first horizontal list named "video_feed_xml_mp4_and_m3u8"'
            'verify if the second item in the first horizontal list in screen is focused',
            RemoteControlKeys.UP,
            accessibility_id
        )

    # @pytest.mark.samsung_tv
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
        self.driver.send_keys([RemoteControlKeys.UP])
        self.building_blocks.screens['Screen Picker'].navigate()

        PRINT('Step 3: verify that the first item in the left menu is focused when screen picker screen opens and after 1 press down')
        accessibility_id = 'focusable-PickerSelector.ScreenPickerContainer.b859d004-d3a2-42e5-8312-260d51d2fa12-PickerItem.94221.0'
        self.driver.send_keys([RemoteControlKeys.UP, RemoteControlKeys.DOWN])
        is_focused = self.driver.is_element_focused(accessibility_id)
        Logger.get_instance().log_assert(is_focused is True,
                                         '%s is not focused' % accessibility_id)

        accessibility_id = 'focusable-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-001-0'
        move_focus_and_verify(
            self.driver,
            4,
            'move focus manager from the first item in menu to the picker component and verify that "video_feed" '
            'item is focused',
            RemoteControlKeys.RIGHT,
            accessibility_id
        )

        accessibility_id = 'focusable-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-003-2'
        move_focus_and_verify(
            self.driver,
            5,
            'move focus manager inside the screen picker grid component and verify that "channel_feed" '
            'becoming focused',
            [RemoteControlKeys.RIGHT, RemoteControlKeys.RIGHT],
            accessibility_id
        )

        accessibility_id = 'focusable-PickerSelector.ScreenPickerContainer.b859d004-d3a2-42e5-8312-260d51d2fa12-PickerItem.94222.1'
        move_focus_and_verify(
            self.driver,
            6,
            'move focus manger to the second tab in the screen picker (screen_2) and verify that screen_2 is focused',
            [RemoteControlKeys.LEFT, RemoteControlKeys.LEFT, RemoteControlKeys.LEFT,
                RemoteControlKeys.DOWN, RemoteControlKeys.ENTER],
            accessibility_id
        )

    @pytest.mark.samsung_tv
    @pytest.mark.usefixtures('automation_driver')
    def test_move_focus_manager_in_top_menu_bar(self):
        self.driver.send_keys(RemoteControlKeys.UP)

        accessibility_id = 'focusable-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a39c93be-3df4-4de0-876d-702833f71664-aed90ff1-9691-4b61-ac2f-d4b917f7d8e9-8-1-a3983053d1ebad89d3d442357a466789-0'
        move_focus_and_verify(
            self.driver,
            1,
            'navigate from top menu bar to "Horizontal List Screen" and verify focus is on "vod_mp4_item_1" item '
            'in "vod_mp4_item_1" Horizontal List component',
            [RemoteControlKeys.UP, RemoteControlKeys.RIGHT,
                RemoteControlKeys.ENTER, RemoteControlKeys.UP, RemoteControlKeys.DOWN],
            accessibility_id
        )

        self.driver.send_keys(RemoteControlKeys.UP)

        accessibility_id = 'focusable-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-bb032301-9eed-4508-8731-61f55041e106-4dc7b914-b36f-42ed-af35-bab04200ada6-9-1-001-0'
        move_focus_and_verify(
            self.driver,
            2,
            'navigate from top menu bar to "Home Screen" and verify focus is on "video_feed" item '
            'in "applicaster cell types json" grid component',
            [RemoteControlKeys.UP, RemoteControlKeys.LEFT,
                RemoteControlKeys.ENTER, RemoteControlKeys.UP, RemoteControlKeys.DOWN],
            accessibility_id
        )

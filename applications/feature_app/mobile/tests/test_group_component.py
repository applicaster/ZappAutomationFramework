
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.utils.logger import Logger

"""
Global Defines
"""
GROUP_COMPONENT_SCREEN = 'GroupComponent'


class GroupComponentTests(BaseTest):
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_group_info_cell(self):
        group_component_screen = self.building_blocks.screens[GROUP_COMPONENT_SCREEN]

        PRINT('Step 1: Navigate to "%s" screen via the side menu' % GROUP_COMPONENT_SCREEN)
        group_component_screen.navigate()

        info_cell_title = 'json_feed'
        PRINT('Step 2: Verify that group info cell with title "%s" is found on the screen' % info_cell_title)
        element = self.driver.find_element_by_text(info_cell_title)
        Logger.get_instance().log_assert(element, 'Group info cell is not found in "%s" screen' % GROUP_COMPONENT_SCREEN)

        PRINT('Step 3: Press on "%s" group info cell and navigate by that to "ListScreen"' % info_cell_title)
        element.click()
        list_screen = self.building_blocks.screens['ListScreen']
        self.driver.wait(list_screen.get_screen_loading_timeout())

        PRINT('     Step 3.1: Verify that the application reached "ListScreen"')
        list_screen.verify_in_screen(retries=5)
        list_screen_item = 'm3u8_vod'
        PRINT('     Step 3.1: Verify that "%s" is showing in "ListScreen"' % list_screen_item)
        element = self.driver.find_element_by_text(list_screen_item, retries=5)
        Logger.get_instance().log_assert(element, 'Failed finding "%s" item after getting to ListScreen from info cell')

        PRINT('Step 4: Verify back navigation from info cell screen to root group screen')
        PRINT('     Step 4.1: Press on the navigation bar back button')
        self.building_blocks.navigation_bar.press_back_button()
        PRINT('     Step 4.2: Verify we reached back to "%s" screen successfully' % GROUP_COMPONENT_SCREEN)
        group_component_screen.verify_in_screen(retries=5)

    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_group_component_items(self):
        group_component_screen = self.building_blocks.screens[GROUP_COMPONENT_SCREEN]

        PRINT('Step 1: Navigate to "%s" screen via the side menu' % GROUP_COMPONENT_SCREEN)
        group_component_screen.navigate()

        PRINT('Step 2: Verify items in the Grid Component of the Group')
        counter = 1
        for title in ('m3u8_vod', 'vod_with_play_next'):
            element = group_component_screen.search_for_item_by_text(title)
            Logger.get_instance().log_assert(
                element,
                'item "%s" in the Groups Grid Component is not found on the screen' % title
            )
            PRINT('     Step 2.%s: item "%s" found on the screen correctly' % (str(counter), title))
            counter += 1

        PRINT('Step 3: Verify items in the Horizontal List Component of the Group')
        element = group_component_screen.search_for_item_by_text('future_program_feed')
        Logger.get_instance().log_assert(
            element,
            'item "future_program_feed" in the Horizontal List Component not found on the screen'
        )
        PRINT('     Step 3.1: item "future_program_feed" found on the screen correctly')

        PRINT('Step 4: Verify items in the List Component of the Group')
        counter = 1
        for title in ('past_program_feed', 'live_channel_feed'):
            element = group_component_screen.search_for_item_by_text(title)
            Logger.get_instance().log_assert(element, 'item "%s" in List Component not found on the screen')
            PRINT('     Step 4.%s: item "%s" found on the screen correctly' % (str(counter), title))
            counter += 1

        PRINT('Step 5: Verify that the Fotter of the Group is displaying correctly')
        element = group_component_screen.search_for_item_by_text('json_feed')
        Logger.get_instance().log_assert(
            element,
            'The fotter of the Group component is not found on the screen'
        )
        PRINT('     Step 5.1: The Fotter is found on the screen correctly')

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_verify_group_info_cell':
            return 'test_verify_group_info_cell:\n' \
               '    TestRail C22947 - Verify the Group ‘Info Cell’ styling in uiBuilder\n' \
               '    TestRail C22955 - Verify connected screen with Group Info Cell\n' \
               '    TestRail C22956 - Verify connected screen with Group component screen\n' \
               '    TestRail C22987 - Verify Navbar functionality within Group Component Screen'
        if test_name == 'test_verify_group_component_items':
            return 'test_verify_group_component_items:\n' \
                   '    TestRail C22988 - Verify each section in Group component screen opens'

        return 'Not Found'

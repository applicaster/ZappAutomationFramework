
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.verifiers.verifier import Verifier
from src.utils.logger import Logger

"""
Global Defines
"""
GROUP_COMPONENT_SCREEN = 'GroupComponent'


class GroupComponentTests(BaseTest):
    
    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_group_info_cell(self):
        group_component_screen = self.building_blocks.screens[GROUP_COMPONENT_SCREEN]

        PRINT('Step 1: Navigate to "%s" screen via the side menu' % GROUP_COMPONENT_SCREEN)
        group_component_screen.navigate()

        # TODO: workaround, we need to cancel here the showing of RN yellow debug
        group_component_screen.dismiss_react_native_yellow_console_box()

        info_cell_title = 'json_feed'
        PRINT('Step 2: Verify that group info cell with title "%s" is found on the screen' % info_cell_title)
        element = self.driver.find_element_by_text(info_cell_title)
        Logger.get_instance().log_assert(element, 'Group info cell is not found in "%s" screen' % GROUP_COMPONENT_SCREEN)

        PRINT('Step 3: Press on "%s" group info cell and navigate by that to "ListScreen"' % info_cell_title)
        element.click()
        list_screen = self.building_blocks.screens['ListScreen']
        self.driver.wait(list_screen.get_screen_loading_timeout())
        # TODO: workaround, we need to cancel here the showing of RN yellow debug
        list_screen.dismiss_react_native_yellow_console_box()

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

    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_group_component_items(self):
        group_component_screen = self.building_blocks.screens[GROUP_COMPONENT_SCREEN]

        PRINT('Step 1: Navigate to "%s" screen via the side menu' % GROUP_COMPONENT_SCREEN)
        group_component_screen.navigate()

    def shortDescription(self) -> str:
        return 'test_verify_group_info_cell:\n' \
               '    TestRail C22947 - Verify the Group ‘Info Cell’ styling in uiBuilder\n' \
               '    TestRail C22955 - Verify connected screen with Group Info Cell\n' \
               '    TestRail C22956 - Verify connected screen with Group component screen\n' \
               '    TestRail C22987 - Verify Navbar functionality within Group Component Screen' \
               '\n' \
               'test_verify_group_component_items:\n' \
               '    TestRail C22988 - Verify each section in Group component screen opens'

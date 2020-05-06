
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.utils.print import PRINT
from src.base_test import BaseTest
from src.verifiers.verifier import Verifier

"""
Global Defines
"""
SCREEN_NAME = 'ScreenWithPreHook'


class ScreenPreHookTests(BaseTest):

    def verify_dummy_pre_hook_screen(self):
        verifier = Verifier(self.driver)
        PRINT('     Verify that pre hook screen is presented correctly')
        verifier.verify_elements_on_screen_by_text(('Quick Brick Hooks test', 'Success', 'Cancel', 'Error'), retries=5)

    @pytest.mark.usefixtures('automation_driver')
    def test_pre_hook_handle_cancel(self):
        screen_with_pre_hook = self.building_blocks.screens[SCREEN_NAME]
        list_screen = self.building_blocks.screens['ListScreen']

        PRINT('Step 1: Navigate to "ListScreen"')
        list_screen.navigate()

        PRINT('Step 2: Navigate to "%s"' % SCREEN_NAME)
        screen_with_pre_hook.navigate(verify_in_screen=False)

        self.verify_dummy_pre_hook_screen()

        PRINT('Step 3: Press on "Cancel" button in order to fall back to "ListScreen"')
        self.driver.find_element_by_text('Cancel').click()
        PRINT('     Step 3.1: Verify we fell back to "ListScreen" screen successfully')
        list_screen.verify_in_screen(retries=5)

    @pytest.mark.usefixtures('automation_driver')
    def test_pre_hook_handle_error(self):
        screen_with_pre_hook = self.building_blocks.screens[SCREEN_NAME]
        list_screen = self.building_blocks.screens['ListScreen']

        PRINT('Step 1: Navigate to "ListScreen"')
        list_screen.navigate()

        PRINT('Step 2: Navigate to "%s"' % SCREEN_NAME)
        screen_with_pre_hook.navigate(verify_in_screen=False)

        self.verify_dummy_pre_hook_screen()

        PRINT('Step 3: Press on "Error" button in order to fall back to "ListScreen"')
        self.driver.find_element_by_text('Error').click()
        PRINT('     Step 3.1: Verify we fell back to "ListScreen" screen successfully')
        list_screen.verify_in_screen(retries=5)

    def test_pre_hook_handle_success(self):
        screen_with_pre_hook = self.building_blocks.screens[SCREEN_NAME]

        PRINT('Step 1: Navigate to "%s"' % SCREEN_NAME)
        screen_with_pre_hook.navigate(verify_in_screen=False)

        self.verify_dummy_pre_hook_screen()

        PRINT('Step 2: Press on "Success" button in order to pass the pre hook and enter the target screen')
        self.driver.find_element_by_text('Success').click()
        PRINT('     Step 2.1: Verify we reached "%s" screen successfully' % SCREEN_NAME)
        screen_with_pre_hook.verify_in_screen(retries=5)

    def shortDescription(self, test_name) -> str:
        return 'TBD'

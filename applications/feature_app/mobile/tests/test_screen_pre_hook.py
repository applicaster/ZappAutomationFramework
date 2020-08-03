
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
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_pre_hook_handle_cancel(self):
        screen_with_pre_hook = self.building_blocks.screens[SCREEN_NAME]
        pre_hook_screen = self.building_blocks.screens['demo_pre_hook']
        list_screen = self.building_blocks.screens['ListScreen']

        PRINT('Step 1: Navigate to "ListScreen"')
        list_screen.navigate()

        PRINT('Step 2: Navigate to "%s"' % SCREEN_NAME)
        screen_with_pre_hook.navigate(verify_in_screen=False)
        pre_hook_screen.verify_in_screen()

        PRINT('Step 3: Press on "Cancel" button in order to fall back to "ListScreen"')
        pre_hook_screen.cancel_enter()
        PRINT('     Step 3.1: Verify we fell back to "ListScreen" screen successfully')
        list_screen.verify_in_screen(retries=5)

    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_pre_hook_handle_error(self):
        screen_with_pre_hook = self.building_blocks.screens[SCREEN_NAME]
        pre_hook_screen = self.building_blocks.screens['demo_pre_hook']
        list_screen = self.building_blocks.screens['ListScreen']

        PRINT('Step 1: Navigate to "ListScreen"')
        list_screen.navigate()

        PRINT('Step 2: Navigate to "%s"' % SCREEN_NAME)
        screen_with_pre_hook.navigate(verify_in_screen=False)
        pre_hook_screen.verify_in_screen()

        PRINT('Step 3: Press on "Error" button in order to fall back to "ListScreen"')
        pre_hook_screen.enter_with_error()
        PRINT('     Step 3.1: Verify we fell back to "ListScreen" screen successfully')
        list_screen.verify_in_screen(retries=5)

    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_pre_hook_handle_success(self):
        screen_with_pre_hook = self.building_blocks.screens[SCREEN_NAME]
        pre_hook_screen = self.building_blocks.screens['demo_pre_hook']

        PRINT('Step 1: Navigate to "%s"' % SCREEN_NAME)
        screen_with_pre_hook.navigate(verify_in_screen=False)
        pre_hook_screen.verify_in_screen()

        PRINT('Step 2: Press on "Success" button in order to pass the pre hook and enter the target screen')
        pre_hook_screen.enter_with_success()
        PRINT('     Step 2.1: Verify we reached "%s" screen successfully' % SCREEN_NAME)
        screen_with_pre_hook.verify_in_screen(retries=5)

    def shortDescription(self, test_name) -> str:
        return 'TBD'

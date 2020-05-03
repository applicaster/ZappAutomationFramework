
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.utils.print import PRINT
from src.base_test import BaseTest
from src.global_defines import RemoteControlKeys


class NavigationBarTests(BaseTest):
    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_back_navigation_from_3rd_screen_to_2nd(self):
        PRINT('Step 1: Navigate to "ListScreen"')
        self.building_blocks.screens['ListScreen'].navigate()

        PRINT('Step 2: Navigate to "GridScreen"')
        self.building_blocks.screens['GridScreen'].navigate()

        PRINT('Step 3: Press the device Back button in order to navigate to "ListScreen"')
        self.driver.send_keys(RemoteControlKeys.BACK)
        PRINT('     Step 3.1: Verify that the application navigated back to "ListScreen"')
        self.building_blocks.screens['ListScreen'].verify_in_screen(retries=5)

    def shortDescription(self, test_name) -> str:
        return 'Verify that the app is navigating to 2nd screen from 3rd screen with the device back button'

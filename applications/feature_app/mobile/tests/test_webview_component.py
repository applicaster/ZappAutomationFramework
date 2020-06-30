
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.utils.logger import Logger

"""
Global Defines
"""
SCREEN_NAME = 'UrlSchemes'


class WebviewComponent(BaseTest):
    @pytest.mark.qb_ios_mobile_nightly
    # @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_webview_component(self):
        screen = self.building_blocks.screens[SCREEN_NAME]

        PRINT('Step 1: Navigate to "%s", that screen has inside a Webview Component' % SCREEN_NAME)
        screen.navigate()

        item_text = 'title_1'
        PRINT('Step 2: Search on the screen for the text "%s" which is found in the webview component html page' % item_text)
        element = screen.search_for_item_by_text(item_text)
        Logger.get_instance().log_assert(element, 'Test could not find "%s" in the webview component html source' % item_text)
        PRINT('     Step 2.1: item "%s" found on the screen correctly' % item_text)

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_verify_webview_component':
            return 'test_verify_webview_component:\n' \
               '    TestRail C23511 - Verify the web view component is loading in the app \n'
        return 'Not Found'

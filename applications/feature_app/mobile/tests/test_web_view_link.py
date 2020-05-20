
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.configuration.configuration import Configuration, PlatformType
from src.utils.logger import Logger


class WebViewTests(BaseTest):
    @pytest.mark.boaz
    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_external_web_view_link(self):
        list_screen = self.building_blocks.screens['ListScreen']

        PRINT('Step 1: Navigate to "ListScreen" screen')
        list_screen.navigate()

        name = 'html_web_view' if Configuration.get_instance().platform_type() == PlatformType.ANDROID else 'Id7'
        PRINT('Step 2: Press on external web view link "%s" item' % name)
        PRINT('     Step 2.1: Start searching for "%s" item' % name)
        element = list_screen.search_for_item_by_text(name)
        PRINT('     Step 2.2: Click on "%s" item' % name)
        element.click()

        timeout = 3
        PRINT('     Step 2.3: Wait %s seconds until that the web page will load' % timeout)
        self.driver.wait(timeout)
        PRINT('     Step 2.4: Finished waiting for the web page to load')

        PRINT('Step 3.0: Verify that the html page is showing correctly')
        text = 'title_1'
        PRINT('     Step 3.1: Verify that "%s" text is showing on the screen' % text)
        element = self.driver.find_element_by_xpath(text, retries=5)
        Logger.get_instance().log_assert(element, 'Test failed to open correctly the external link web view')
        PRINT('     Step 3.2: External link web view opened correctly')

        PRINT('Step 4.0: Test back functionality from web view screen')
        PRINT('     Step 4.1: Press on the navigation bar back button')
        self.building_blocks.navigation_bar.press_back_button()
        PRINT('     Step 4.2: Verify that the application navigated back to ListScreen')
        list_screen.verify_in_screen(retries=7)

    def shortDescription(self, test_name) -> str:
        return 'test_verify_external_web_view_link:\n' \
               '    TestRail C22993 - Verify general functionality of the Webview\n' \
               '    TestRail C22991 - Verify that URL is clickable in a cell\n' \
               '    TestRail C22994 - Verify Navbar functionality within the Webview screen'

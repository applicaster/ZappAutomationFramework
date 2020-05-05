
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.utils.print import PRINT
from src.base_test import BaseTest
from src.verifiers.verifier import Verifier
from src.utils.logger import Logger


class SearchPluginTests(BaseTest):
    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_search_fall_back_screen(self):
        verifier = Verifier(self.driver)
        PRINT('Step 1: Open search screen from the home screen navigation bar icon')
        self.building_blocks.navigation_bar.press_right_button_by_position(1)

        PRINT('Step 2: Verify that the fall back screen results are showing on the screen correctly')
        verifier.verify_elements_on_screen_by_text('url_scheme_to_screen', retries=5)

    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_basic_search(self):
        search_screen = self.building_blocks.screens['search_screen']
        verifier = Verifier(self.driver)

        PRINT('Step 1: Open search screen from the home screen navigation bar icon')
        self.building_blocks.navigation_bar.press_right_button_by_position(1)

        search_text = 'Boy'
        PRINT('Step 2: Search and verify results for "%s"' % search_text)
        PRINT('     Step 2.1: Open the keyboard by typing the search area')
        search_screen.open_keyboard()

        PRINT('     Step 2.2: Search for "%s" text' % search_text)
        search_screen.search(search_text)
        search_screen.press_enter_in_search()

        results = ('About a Boy', 'The Last Boy Scout')
        PRINT('Step 3: Verify that the results for "%s"' % str(results))
        verifier.verify_elements_on_screen_by_text(results, retries=7)

    @pytest.mark.qb_android_mobile
    @pytest.mark.usefixtures('automation_driver')
    def test_verify_search_empty_results(self):
        search_screen = self.building_blocks.screens['search_screen']

        PRINT('Step 1: Open search screen from the home screen navigation bar icon')
        self.building_blocks.navigation_bar.press_right_button_by_position(1)

        search_text = 'BoyAAAAAA'
        PRINT('Step 2: Search and verify results for "%s"' % search_text)
        PRINT('     Step 2.1: Open the keyboard by typing the search area')
        search_screen.open_keyboard()

        PRINT('     Step 2.2: Search for "%s" text' % search_text)
        search_screen.search(search_text)
        search_screen.press_enter_in_search()

        PRINT('Step 3: Verify that the results for "Boy" search not showing on screen when searching for "%s"'
              % str(search_text))
        Logger.get_instance().log_assert(
            self.driver.find_element_by_text('About a Boy', retries=3) is None,
            'Application did not show empty results when user searched for "%s"' % search_text
        )

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_search_fall_back_screen':
            return 'TestRail C22898 - Verify fall back screen and basic search functionality'

        elif test_name == 'test_verify_search_empty_results':
            return 'TestRail C22899 - Verify that 0 results are showing when user searching for text which that not exits'

        elif test_name == 'test_verify_basic_search':
            return 'TestRail C22900 - Verify that the search keyboard is closing when the user scrolling inside the search results\n' \
                   'TestRail C22898 - Verify fall back screen and basic search functionality'

        elif test_name == 'test_verify_search_clear_button':
            return 'TestRail C22901 - Verify that the clear button is working correctly'

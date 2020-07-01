
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.base_test import BaseTest, PRINT
from src.utils.logger import Logger

"""
Global Defines
"""
FAVORITES_ICON_TAG = 'local_storage_favourites_action_%s'
NO_FAVORITES_TITLE = "You don't have any favourites"
ADD_REMOVE_FAVORITES_ANIMATION = 3
APP_BOOT_TIMEOUT = 18


class FavouritesTests(BaseTest):
    def add_item_to_favourites(self, item_name, step):
        list_screen = self.building_blocks.screens['ListScreen']

        PRINT('Step %s: Search the screen for the favorite button of "%s" item' % (step, item_name))
        element = list_screen.search_for_item_by_id(FAVORITES_ICON_TAG % item_name)
        Logger.get_instance().log_assert(element,
                                         'Test could not find the favorite button for "%s" on the screen' % item_name)
        PRINT('     Step %s.1: Favorite button of "%s" item found on the screen successfully' % (step, item_name))
        PRINT('     Step %s.2: Press on the favorites button of "%s" item' % (step, item_name))
        element.click()
        self.driver.wait(ADD_REMOVE_FAVORITES_ANIMATION)
        PRINT('     Step %s.3: Adding item %s to favourites completed' % (step, item_name))

    def remove_item_from_favourites(self, item_name, step):
        list_screen = self.building_blocks.screens['ListScreen']
        PRINT('Step %s.1: Remove item "%s" from favorites' % (step, item_name))
        element = list_screen.search_for_item_by_id(FAVORITES_ICON_TAG % item_name)
        element.click()
        self.driver.wait(ADD_REMOVE_FAVORITES_ANIMATION)
        PRINT('Step %s.2: Item removed from favourites' % item_name)

    @pytest.mark.qb_ios_mobile_nightly
    @pytest.mark.qb_android_mobile_nightly
    @pytest.mark.usefixtures('automation_driver')
    def test_add_and_remove_from_favourites(self):
        list_screen = self.building_blocks.screens['ListScreen']
        favorites_screen = self.building_blocks.screens['Favorites']

        PRINT('Step 1: Navigate to ListScreen')
        list_screen.navigate()

        json_feed_item_name = 'm3u8_vod'
        cms_item_name = 'vod_0'
        self.add_item_to_favourites(json_feed_item_name, 2)
        self.add_item_to_favourites(cms_item_name, 3)

        PRINT('Step 4: Relaunch application')
        self.driver.restart_application()
        PRINT('     Step 4.1: Wait up to %s seconds until the application will get to home screen' % APP_BOOT_TIMEOUT)
        self.building_blocks.screens['Home'].verify_in_screen(retries=APP_BOOT_TIMEOUT)
        PRINT('     Step 4.2: Application finished restarting successfully')

        PRINT('Step 5: Navigate from the side menu to Favorites screen')
        favorites_screen.navigate()

        self.remove_item_from_favourites(json_feed_item_name, 6)
        self.remove_item_from_favourites(cms_item_name, 7)

        element = self.driver.find_element_by_text(NO_FAVORITES_TITLE, retries=3)
        Logger.get_instance().log_assert(element, 'No favorites message: "%s" is not found on screen' % NO_FAVORITES_TITLE)

    def shortDescription(self, test_name) -> str:
        if test_name == 'test_add_and_remove_from_favorites':
            return 'test_add_and_remove_from_favorites:' \
                   '    TestRail: C22970 - Verify adding to Favorites CMS VOD item\n'\
                   '    TestRail: C22972 - Verify adding to Favorites json feed VOD item\n'\
                   '    TestRail: C23006 - Verify removing item from Favorites screen\n'
        return 'Not Found'

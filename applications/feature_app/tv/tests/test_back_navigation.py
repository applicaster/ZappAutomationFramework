import pytest

from src.automation_manager.automation_manager import automation_driver
from src.global_defines import RemoteControlKeys, PlatformType
from src.utils.logger import Logger
from src.configuration.configuration import Configuration
from src.utils.print import PRINT
from src.base_test import BaseTest


@pytest.mark.tv_apps_sanity
@pytest.mark.usefixtures('automation_driver')
class BackNavigationsBetweenScreenTest(BaseTest):
    def navigate_to_next_screen(self):
        self.driver.send_keys([RemoteControlKeys.UP, RemoteControlKeys.RIGHT, RemoteControlKeys.ENTER, 4], 2)

    def test_back_navigation_between_screens(self):
        PRINT('Step 1: Navigate to "Horizontal List Screen"')
        self.navigate_to_next_screen()
        self.building_blocks.screens['Horizontal List Screen'].verify_in_screen()

        PRINT('Step 2: Navigate to "Hero Screen"')
        self.navigate_to_next_screen()
        self.building_blocks.screens['Hero Screen'].verify_in_screen()

        PRINT('Step 3: Navigate back "Home" with the Back button')
        self.driver.send_keys(RemoteControlKeys.BACK)
        self.building_blocks.screens['Home'].verify_in_screen()

    def shortDescription(self):
        return 'C17449 - Verify navigating between 3 screen'


@pytest.mark.tv_apps_sanity
@pytest.mark.usefixtures('automation_driver')
class BackNavigationFromScreenPickerTest(BaseTest):
    def test_back_navigation_from_screen_picker(self):
        PRINT('Step 1: Navigate to "Screen Picker"')
        self.building_blocks.screens['Screen Picker'].navigate()

        PRINT('Step 2: Navigate to the second tab in the "Screen 2" in screen picker tabs')
        self.driver.send_keys([RemoteControlKeys.DOWN, RemoteControlKeys.ENTER], 2)

        PRINT('Step 3: Press the Back button')
        self.driver.send_keys(RemoteControlKeys.BACK)

        PRINT('Step 4: Verify that the user is back again in Home screen')
        self.building_blocks.screens['Home'].verify_in_screen()

    def shortDescription(self):
        return 'C17451 - Verify navigating inside Screen Picker tabs'

@pytest.mark.boaz
@pytest.mark.tv_apps_sanity
@pytest.mark.android_tv
@pytest.mark.usefixtures('automation_driver')
class BackNavigationFromPlayerTest(BaseTest):
    def test_back_navigation_from_player(self):
        PRINT('Step 1: Navigate to "Horizontal List Screen"')
        self.building_blocks.screens['Horizontal List Screen'].navigate()

        PRINT('Step 2: Play vod item "vod_mp4_item_1" and navigate by that to the player screen')
        self.driver.send_keys([RemoteControlKeys.DOWN, RemoteControlKeys.ENTER])
        self.driver.wait(7)

        PRINT('Step 3: Press Back button from player screen')
        self.driver.send_keys(RemoteControlKeys.BACK)

        PRINT('Step 4: Verify that the application is now in "Horizontal List Screen" after navigating back')
        self.building_blocks.screens['Horizontal List Screen'].verify_in_screen(retries=10)

    def shortDescription(self):
        return 'C17452 - Verify navigating back from player screen'


@pytest.mark.tv_apps_sanity
@pytest.mark.android_tv
@pytest.mark.usefixtures('automation_driver')
class BackNavigationFromConnectedScreenTest(BaseTest):
    def test_back_navigation_from_connected_screen(self):
        platform_type = Configuration.get_instance().platform_type()

        remote_control_actions = []
        if platform_type == PlatformType.ANDROID_TV:
            timeout = 2
            # 7 times on down button
            for i in range(7):
                remote_control_actions.append(RemoteControlKeys.DOWN)

        elif platform_type == PlatformType.WEB:
            timeout = 0.7
            # 13 times on down button
            for i in range(13):
                remote_control_actions.append(RemoteControlKeys.DOWN)

        PRINT('Step 1: Navigate to "Collection Of Collections" component, press on the remote down button')
        self.driver.send_keys(remote_control_actions, timeout)

        PRINT('Step 2: Open "Collection Child 1"')
        self.driver.send_keys(RemoteControlKeys.ENTER)
        self.driver.wait(2)

        PRINT('Step 3: Verify that the VOD items of Collection 1 are displaying correctly')
        items = ['vod_3', 'vod_2', 'vod_1']
        index = 0
        for item in items:
            index += 1
            element = self.driver.find_element_by_text(item, retries=5)
            Logger.get_instance().log_assert(element, 'Test failed to find "%s" on screen' % item)
            PRINT('     Step 5.%s: Item %s found on screen' % (str(index), item))

        PRINT('Step 4: Press Back button in order to get out of the child connect screen')
        self.driver.send_keys(RemoteControlKeys.BACK)
        self.driver.wait(2)

        PRINT('Step 5: Verify navigation back navigated the user to Home screen')
        self.building_blocks.screens['Home'].verify_in_screen(retries=7)
        element = self.driver.find_element_by_text('applicaster_cell_types', retries=7)
        Logger.get_instance().log_assert(element, 'Test failed to find "%s" inside Home screen' % item)

    def shortDescription(self):
        return 'C17453 - Verify navigation back from a connected screen to home screen'

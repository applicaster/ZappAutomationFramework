
from applications.feature_app.feature_app_player import FeatureAppPlayer
from src.generic_building_blocks.building_blocks_interface import BuildingBlocksInterface
from src.generic_building_blocks.tv.tv_screen import TvScreen
from applications.feature_app.tv.building_blocks.home_screen import HomeScreen
from src.utils.print import PRINT
from src.global_defines import RemoteControlKeys, PlatformType
from src.configuration.configuration import Configuration
from src.utils.logger import Logger


class BuildingBlocks(BuildingBlocksInterface):
    def boot_step(self):
        boot_timeout = 136
        PRINT('Start waiting for home screen to load')
        element = None
        for i in range(boot_timeout):
            element = self.test.driver.find_element_by_text('applicaster_cell_types')
            if element is not None:
                break
            self.test.driver.wait(1)
        PRINT('Finish waiting for home screen to load')
        Logger.get_instance().log_assert(element is not None, 'Application failed launching to home screen correctly')

        self.test.driver.wait(10)

        if Configuration.get_instance().platform_type() == PlatformType.TV_OS:
            PRINT(
                'Workaround: navigate 2 times Down,'
                ' that is for solving https://applicaster.atlassian.net/browse/ZPP-2279', text_color='magenta')
            self.test.driver.send_keys([RemoteControlKeys.DOWN, RemoteControlKeys.DOWN], 4)

        return True

    def __setup_building_blocks__(self):
        self.screens['Home'] = HomeScreen(
            self.test,
            'Home'
        )

        screens = (
            ('Horizontal List Screen', [RemoteControlKeys.UP, RemoteControlKeys.RIGHT, RemoteControlKeys.ENTER]),
            ('Hero Screen',
             [RemoteControlKeys.UP, RemoteControlKeys.RIGHT, RemoteControlKeys.RIGHT, RemoteControlKeys.ENTER]),
            ('Mixed Screen',
             [RemoteControlKeys.UP, RemoteControlKeys.RIGHT, RemoteControlKeys.RIGHT, RemoteControlKeys.RIGHT,
              RemoteControlKeys.ENTER]),
            ('Screen Picker',
             [RemoteControlKeys.UP, RemoteControlKeys.RIGHT, RemoteControlKeys.RIGHT, RemoteControlKeys.RIGHT,
              RemoteControlKeys.RIGHT, RemoteControlKeys.ENTER]),
        )
        for screen in screens:
            self.screens[screen[0]] = TvScreen(self.test, screen[0], navigation_steps=screen[1])

        self.screens['player_screen'] = FeatureAppPlayer(self.test)

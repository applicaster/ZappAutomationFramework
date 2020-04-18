
from src.generic_building_blocks.building_blocks_interface import BuildingBlocksInterface
from src.utils.print import PRINT
from src.configuration.configuration import Configuration
from src.global_defines import PlatformType


class BuildingBlocks(BuildingBlocksInterface):

    def boot_step(self):
        platform = Configuration.get_instance().platform_type()
        boot_timeout = 25

        if platform == PlatformType.ANDROID:
            boot_timeout = 90

        if platform == PlatformType.IOS:
            boot_timeout = 60

        self.__wait_for_home_screen_to_load__(boot_timeout)

    def __wait_for_home_screen_to_load__(self, boot_timeout=25):
        PRINT('Start waiting for home screen to load')
        home_screen_accessbility_id = 'be7549ab-c5e9-4dff-a0a2-fa8c887cdf8d'
        element = self.test.driver.find_element_by_accessibility_id(home_screen_accessbility_id, retries=boot_timeout)
        PRINT('Finish waiting for home screen to load')
        if element is None:
            raise Exception('Application failed finding "%s" home screen accessibility identifier after launch'
                            % home_screen_accessbility_id)

        self.test.driver.wait(5)

    def __setup_building_blocks__(self):
        pass


from src.generic_building_blocks.building_blocks_interface import BuildingBlocksInterface
from src.utils.print import PRINT

"""
Global Defines
"""
BOOT_TIMEOUT = 90


class BuildingBlocks(BuildingBlocksInterface):
    """
    Public Implementation
    """
    def boot_step(self):
        PRINT('Start waiting for home screen to load')
        home_screen_accessbility_id = 'be7549ab-c5e9-4dff-a0a2-fa8c887cdf8d'
        element = self.test.driver.find_element_by_accessibility_id(home_screen_accessbility_id, retries=BOOT_TIMEOUT)
        PRINT('Finish waiting for home screen to load')
        if element is None:
            raise Exception('Application failed finding "%s" home screen accessibility identifier after launch'
                            % home_screen_accessbility_id)

        self.test.driver.wait(5)

    """
    Private Implementation
    """
    def __setup_building_blocks__(self):
        pass

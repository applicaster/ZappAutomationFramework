
from src.generic_building_blocks.building_blocks_interface import BuildingBlocksInterface
from src.utils.print import PRINT


class BuildingBlocks(BuildingBlocksInterface):

    def boot_step(self):
        PRINT('Start waiting for home screen to load')
        text_to_find = 'video_feed'
        element = self.driver.find_element_by_text(text_to_find, retries=30)
        PRINT('Finish waiting for home screen to load')
        if element is None:
            raise Exception('Application failed finding "%s" text on Home after launch' % text_to_find)
        return True

    def __setup_building_blocks__(self):
        pass

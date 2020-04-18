
from src.generic_building_blocks.tv.tv_screen import TvScreen
from src.global_defines import PlatformType
from src.configuration.configuration import Configuration


class HomeScreen(TvScreen):
    """
    Public Implementation
    """
    def navigate(self):
        if Configuration.get_instance().platform_type() == PlatformType.WEB:
            self.test.driver.refresh()
            self.test.driver.wait(6)

    """
    Private Implementation
    """
    def __init__(self, test, screen_name):
        TvScreen.__init__(self, test, screen_name)

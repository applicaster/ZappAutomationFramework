
import unittest
from importlib.util import spec_from_file_location, module_from_spec

from src.global_defines import ROOT_DIR
from src.utils.print import PRINT
from src.utils.logger import Logger
from src.configuration.configuration import Configuration


'''
Global Defines
'''
TEST_START_RUNNING = '\n===============| Test "%s" Started Running |==============='
TEST_FINISHED_RUNNING = '===============| Test "%s" Finished Running |===============\n'


class BaseTest(unittest.TestCase):
    """
    Public Implementation
    """
    def setUp(self):
        super(BaseTest, self).setUp()
        PRINT(TEST_START_RUNNING % self._testMethodName, 'green')

        # Boot step 0: Setup logger
        Logger.get_instance().initialization(self)

        # Boot step 1: Open application
        PRINT('Step 0.1: Open application')
        self.__activate_app__()

        # Boot step 2: Init the needed building blocks for test
        self.__setup_building_blocks__()

        # Boot step 3: Run ui boot steps
        self.__ui_boot_step__()

    def tearDown(self):
        super(BaseTest, self).tearDown()
        self.__tear_down_actions__()
        PRINT(TEST_FINISHED_RUNNING % self._testMethodName, 'green')

    """
    Private Implementation
    """
    def __activate_app__(self):
        try:
            self.driver.activate_app()
        except Exception as exp:
            self.__tear_down_actions__()
            self.assertEqual(0, 1, exp)

    def __ui_boot_step__(self):
        try:
            self.building_blocks.boot_step()
        except Exception as exp:
            self.__tear_down_actions__()
            self.assertEqual(0, 1, exp)

    def __setup_building_blocks__(self):
        try:
            building_blocks_path = Configuration.get_instance().get('general', 'building_blocks')
            spec = spec_from_file_location('BuildingBlocks', '%s/%s' % (ROOT_DIR, building_blocks_path))
            building_blocks_module = module_from_spec(spec)
            spec.loader.exec_module(building_blocks_module)
            self.building_blocks = building_blocks_module.BuildingBlocks(self)
        except Exception as exp:
            self.__tear_down_actions__()
            self.assertEqual(0, 1, 'Application failed on setup the test building blocks: %s' % exp)

    def __tear_down_actions__(self):
        PRINT('Final Step: Kill application')
        Logger.get_instance().take_screenshot('tear_down')
        Logger.get_instance().close_logs()
        self.driver.terminate_app()

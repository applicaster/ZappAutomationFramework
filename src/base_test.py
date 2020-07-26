
import unittest
from importlib.util import spec_from_file_location, module_from_spec

from src.global_defines import ROOT_DIR
from src.utils.print import PRINT
from src.utils.logger import Logger
from src.configuration.configuration import Configuration

from src.analytics.analytics_manager import AnalyticsManager


'''
Global Defines
'''
TEST_START_RUNNING = '\n================| Test "%s" Started Running |================'
TEST_FINISHED_RUNNING = '================| Test "%s" Finished Running |================\n'


class BaseTest(unittest.TestCase):
    """
    Public Implementation
    """
    def setUp(self):
        super(BaseTest, self).setUp()
        PRINT(TEST_START_RUNNING % self._testMethodName, 'green')

        PRINT('Test Description:', text_color='green', attributes=['underline'])
        PRINT('%s\n' % self.shortDescription(self._testMethodName))

        # Boot step 0: Setup logger
        Logger.get_instance().initialization(self)

        PRINT('"%s" Steps:' % self._testMethodName, text_color='green', attributes=['underline'])

        # Boot step 1: Open application
        PRINT('Step 0: Open application')
        self.__activate_app__()

        # Boot step 2: Init the needed building blocks for test
        self.__setup_building_blocks__()

        # Boot step 3: Init analytics manager
        self.__setup_analytics_manager__()

        # Boot step 4: Run ui boot steps
        self.__ui_boot_step__()

    def tearDown(self):
        super(BaseTest, self).tearDown()
        self.__tear_down_actions__()
        PRINT(TEST_FINISHED_RUNNING % self._testMethodName, 'green')

    def shortDescription(self, test_name) -> str:
        return 'Not Found, TBD'

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
        """
        # When pytest start running at test its performing a few boot steps that found in BaseTestboot sequence,
        # some of them are a UI actions and some are just initialising the test it self.
        # In one of the steps its doing a call to boot_step() method that is must be override as part of the
        # building_blocks.py file.
        # For more info read here:
        # https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/1042022816/Building+Blocks
        """
        try:
            self.building_blocks.boot_step()
        except Exception as exp:
            self.__tear_down_actions__()
            self.assertEqual(0, 1, exp)

    def __setup_building_blocks__(self):
        """
        # For more info about this method read here:
        # https://applicaster.atlassian.net/wiki/spaces/~794659641/pages/1042022816/Building+Blocks
        # :return: None
        """
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

    def __setup_analytics_manager__(self):
        """
        # Analytics manager object is being setup only if the tester added in the config.cfg file pointer to some log
        # file. Analytics manager idea is to search for events inside log file. The manager assumes that a line with
        # prefix of AutomationAnalyticsEvent contain inside analytic event.
        # :return: None
        """
        if Configuration.get_instance().get('general', 'yarn_server_log'):
            self.analytics_manager = AnalyticsManager()

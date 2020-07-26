
from src.utils.logger import Logger
from src.utils.print import PRINT
from src.configuration.configuration import Configuration

from json import loads

'''
Global Defines
'''
EVENT_PREFIX = 'AutomationAnalyticsEvent'


class AnalyticsManager(object):
    """
    Public Implementation
    """
    def verify_events(self, events):
        if isinstance(events, dict):
            events = [events]

        log = self.__get_log__()
        for test_event in events:
            event_found = False
            for line in log:
                if self.event_prefix_ in line:
                    log_event = loads(line.split(self.event_prefix_)[1])
                    if test_event.items() == log_event.items():
                        event_found = True
                        break
            Logger.get_instance().log_assert(
                event_found,
                'Analytic event "%s" was not reported during the test run,\nDifference found in: %s'
                % (test_event, test_event.items() - log_event.items())
            )
            PRINT('Analytics following analytic event reported correctly:')
            PRINT(test_event, text_color='white')

        return True

    def print_events(self):
        log = self.__get_log__()
        for line in log:
            if self.event_prefix_ in line:
                print(line)

    """
    Private Implementation
    """
    def __init__(self,
                 log_file_path=Configuration.get_instance().get('general', 'yarn_server_log'),
                 event_prefix=EVENT_PREFIX):
        self.log_file_path_ = log_file_path
        self.event_prefix_ = event_prefix

    def __get_log__(self):
        return open(self.log_file_path_, 'r')


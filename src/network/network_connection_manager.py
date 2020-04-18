
from threading import Lock
from src.utils.logger import Logger


class ConnectionType(object):
    NONE = 0
    AIRPLAIN_MODE = 1
    WIFI_ONLY = 2
    DATA_ONLY = 4
    ALL_NETWORK_ON = 6

class NetworkConnectionManager(object):
    '''
    Public Implementation
    '''
    def is_wifi_on(self):
        on = False

        self.lock_.acquire()
        network_connection = self.driver_.network_connection
        if network_connection == ConnectionType.ALL_NETWORK_ON:
            on = True
        self.lock_.release()

        return on

    def turn_on_wifi(self):
        if self.get_network_connection_state() != ConnectionType.ALL_NETWORK_ON:
            self.driver_.toggle_wifi()

            Logger.get_instance().info(self, 'turn_on_wifi', 'Network switched to ALL_NETWORK_ON')

    def turn_off_wifi(self):
        if self.get_network_connection_state() != ConnectionType.DATA_ONLY:
            self.driver_.toggle_wifi()
            Logger.get_instance().info(self, 'turn_on_wifi', 'Network switched to DATA_ONLY')

    def toggle_wifi(self):
        self.driver.toggle_wifi()

    def get_network_connection_state(self):
        network_connection_type = None

        network_connection = self.driver_.network_connection
        if network_connection == ConnectionType.ALL_NETWORK_ON:
            network_connection_type = ConnectionType.ALL_NETWORK_ON

        elif network_connection == ConnectionType.DATA_ONLY:
            network_connection_type = ConnectionType.DATA_ONLY

        elif network_connection == ConnectionType.AIRPLAIN_MODE:
            network_connection_type = ConnectionType.AIRPLAIN_MODE

        elif network_connection == ConnectionType.WIFI_ONLY:
            network_connection_type = ConnectionType.WIFI_ONLY

        return network_connection_type

    @staticmethod
    def __supported_connections_types__():
        return [ConnectionType.AIRPLAIN_MODE,
                ConnectionType.ALL_NETWORK_ON,
                ConnectionType.DATA_ONLY,
                ConnectionType.WIFI_ONLY]

    def __set_network_connection__(self, new_connection_state):
        if new_connection_state not in NetworkConnectionManager.supported_connections_types():
            return

        self.lock_.acquire()
        res = self.get_network_connection_state()
        if res != new_connection_state:
            self.driver_.set_network_connection(new_connection_state)
        self.lock_.release()

    '''
    Private Implementation 
    '''
    def __init__(self, driver):
        self.driver_ = driver
        self.lock_ = Lock()
        self.turn_on_wifi()


import configparser
from src.global_defines import ROOT_DIR
from src.global_defines import PlatformType

'''
Global Defines
'''
BASE_CONFIG_PATH = '%s/base_config.cfg' % ROOT_DIR
CONFIG_PATH = '%s/config.cfg' % ROOT_DIR


class Configuration(object):
    __instance = None
    """
    Public Implementation
    """
    @staticmethod
    def get_instance():
        """ Static access method. """
        if Configuration.__instance is None:
            Configuration()

        return Configuration.__instance

    def get(self, section, option):
        try:
            value = self.config.get(section, option)
            if value.lower() in ('true', '1', 'yes'):
                return True

            elif value.lower() in ('false', '0', 'no'):
                return False
            else:
                return value
        except Exception as exp:
            pass


    def platform_type(self):
        platform = str(self.get('general', 'platform')).lower()

        if platform == PlatformType.IOS:
            return PlatformType.IOS

        if platform == PlatformType.TV_OS:
            return PlatformType.TV_OS

        if platform == PlatformType.ANDROID:
            return PlatformType.ANDROID

        if platform == PlatformType.ANDROID_TV:
            return PlatformType.ANDROID_TV

        if platform == PlatformType.WEB:
            return PlatformType.WEB

    def get_bundle_id(self):
        platform = self.platform_type()

        if platform in (PlatformType.IOS, PlatformType.TV_OS):
            return self.get('appium', 'bundleId')

        if platform in (PlatformType.ANDROID, PlatformType.ANDROID_TV):
            return self.get('appium', 'appPackage')

        if platform == PlatformType.WEB:
            return self.get('general', 'bundle_id')

    def get_section(self, section):
        values = {}
        for key in self.config.options(section):
            values[key] = self.get(section, key)
        return values

    """
    Private Implementation
    """
    def __init__(self):
        """ Virtually private constructor. """
        if Configuration.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            Configuration.__instance = self
            self.__load_configuration_files__()

    def __load_configuration_files__(self):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read([BASE_CONFIG_PATH, CONFIG_PATH])

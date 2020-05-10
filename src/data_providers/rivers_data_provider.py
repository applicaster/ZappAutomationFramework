
from json import loads

from src.configuration.configuration import Configuration
from src.global_defines import PlatformType
from src.global_defines import UIBuilderScreensTypes
from src.utils.logger import Logger
from src.network.http_client import HttpClient


class RiversDataProvider(object):
    __instance = None
    RIVERS_URL = 'https://assets-secure.applicaster.com/zapp/accounts/%s/apps/%s/%s/%s/rivers/rivers.json'

    """
    Public Implementation 
    """
    @staticmethod
    def get_instance():
        """ Static access method. """
        if RiversDataProvider.__instance is None:
            RiversDataProvider()

        return RiversDataProvider.__instance

    def get_data(self):
        return self.rivers_dict_

    def get_home_node(self):
        for screen in self.rivers_dict_:
            if screen['home'] is True:
                return screen

    def get_top_menu_bar_tv_items(self, by_title=True):
        items = []
        for screen in self.rivers_dict_:
            if screen['home'] is True:
                for navigation in screen['navigations']:
                    if navigation['navigation_type'] == 'top_menu_bar_tv':
                        if by_title:
                            for item in navigation['nav_items']:
                                items.append(item['title'])
                        else:
                            items = navigation['nav_items']
                        break
        return items

    def get_side_menu_items(self, by_title=True):
        items = []
        for screen in self.rivers_dict_:
            if screen['home'] is True:
                for navigation in screen['navigations']:
                    if navigation['navigation_type'] == 'quick_brick_side_menu':
                        if by_title:
                            for item in navigation['nav_items']:
                                items.append(item['title'])
                        else:
                            items = navigation['nav_items']
                        break
        return items

    def get_ui_builder_screens(self, specific_type=None):
        screens = []
        for screen in self.rivers_dict_:
            if specific_type is not None and screen['type'] == specific_type:
                screens.append(screen)
            elif screen['type'] in UIBuilderScreensTypes.get_types_array():
                screens.append(screen)
        return screens

    def get_navigation_bar_items_for_screen(self, screen_id=None):
        screen_id = screen_id if screen_id is not None else self.get_home_node()['id']
        items = []
        for screen in self.rivers_dict_:
            if screen['id'] == screen_id:
                for item in screen['navigations']:
                    if 'category' in item:
                        if item['category'] == 'nav_bar':
                            for nav_bar_item in item['nav_items']:
                                items.append(nav_bar_item)
        return items

    def get_navigation_item(self, navigation_type, item_title):
        home_node = self.get_home_node()
        for navigation in home_node['navigations']:
            if navigation['navigation_type'] == navigation_type:
                for nav_item in navigation['nav_items']:
                    if nav_item['title'] == item_title:
                        return nav_item

    def get_navigation_bar_id_by_name(self, screen_name, navigation_bar_item_name):
        for screen in self.rivers_dict_:
            if (screen['name'] == screen_name) and (screen_name in screen['name']) and ('navigations' in screen):
                for screen_navigation in screen['navigations']:
                    if screen_navigation['navigation_type'] == 'applicaster_toolbar' and screen_navigation['category'] == 'nav_bar':
                        for navigation_bar_item in screen_navigation['nav_items']:
                            if 'title' in navigation_bar_item and navigation_bar_item['title'] == navigation_bar_item_name:
                                return navigation_bar_item['id']
        return None

    """
    Private Implementation 
    """
    def __init__(self):
        """ Virtually private constructor. """
        if RiversDataProvider.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            RiversDataProvider.__instance = self
            self.rivers_dict_ = None
            self.__setup__()

    def __fetch_rivers_data__(self):
        app_id = Configuration.get_instance().get('general', 'app_id')
        app_version = Configuration.get_instance().get('general', 'app_version')
        bundle_id = Configuration.get_instance().get_bundle_id().replace('com.applicaster.ent.', '')
        store = self.__get_store_url_param__()
        url = self.RIVERS_URL % (app_id, bundle_id, store, app_version)
        Logger.get_instance().info(self, '__fetch_rivers_data__', 'url: %s' % str(url))

        response = HttpClient().do_get(url, retries=7)
        return loads(response.content)

    def __get_store_url_param__(self):
        platform = Configuration.get_instance().platform_type()

        if platform in (PlatformType.IOS, PlatformType.TV_OS):
            return 'apple_store'

        if platform in (PlatformType.ANDROID, PlatformType.ANDROID_TV):
            return 'google_play'

        if platform in PlatformType.WEB:
            return 'samsung_app_store'

    def __setup__(self):
        self.rivers_dict_ = self.__fetch_rivers_data__()

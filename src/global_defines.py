
from os import path

ROOT_DIR = '%s/..' % path.dirname(path.abspath(__file__))


class PlatformType(object):
    """
    Platform types
    """
    IOS = 'ios'
    ANDROID = 'android'
    ANDROID_TV = 'android_tv'
    TV_OS = 'tv_os'
    WEB = 'web'


class RemoteControlKeys(object):
    """
    This enum should be used once a test sends a keycode (used from test side)
    """
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'down'
    ENTER = 'enter'
    HOME = 'home'
    BACK = 'back'


class BrowserTypes(object):
    """
    Linux supported web browsers
    """
    CHROME = 'chrome'
    FIREFOX = 'firefox'


class SwipeArea(object):
    """
    Enum for describing swipe area: bottom, top, center
    """
    TOP = 'top'
    CENTER = 'center'
    BOTTOM = 'bottom'


class Direction(object):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class ScreenType(object):
    UI_BUILDER_SCREEN = 'ui_builder_screen'
    STANDALONE_SCREEN = 'standalone_screen'


class UIBuilderScreensTypes(object):
    """
    Enum for classifying the UIBuilder types of screens
    """
    GENERAL_CONTENT = 'general_content'

    @staticmethod
    def get_types_array():
        return [UIBuilderScreensTypes.GENERAL_CONTENT]
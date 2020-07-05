
from src.generic_building_blocks.player_screen import PlayerScreen
from src.generic_building_blocks.player_screen import PlayerDefaultAccessibilityIdentifiers
from src.generic_building_blocks.player_screen import DEFAULT_HIDE_CONTROLS_TIMEOUT
from src.base_test import PRINT

"""
Global Defines
"""
SHOW_CONTROLS_ANIMATION_DURATION = 0.4


class AppPlayerInterface(object):
    """
    Public Implementation
    """
    def play_button_accessibility_identifier(self): raise NotImplementedError
    def pause_button_accessibility_identifier(self): raise NotImplementedError
    def rew_button_accessibility_identifier(self): raise NotImplementedError
    def ffwd_button_accessibility_identifier(self):raise NotImplementedError
    def close_button_accessibility_identifier(self): raise NotImplementedError
    def progress_bar_accessibility_identifier(self): raise NotImplementedError
    def hide_controls_timeout(self): raise NotImplementedError
    def get_screen_id(self): raise NotImplementedError

    """
    Private Implementation
    """
    def __init__(self, driver):
        self.driver = driver


class JwPlayer(AppPlayerInterface):
    """
    Public Implementation
    """
    def play_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.PLAY_PAUSE_BUTTON_ACCESSIBILITY_ID

    def pause_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.PAUSE_BUTTON_ACCESSIBILITY_ID

    def rew_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.REW_BUTTON_ACCESSIBILITY_ID

    def ffwd_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.FFWD_BUTTON_ACCESSIBILITY_ID

    def close_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.CLOSE_BUTTON_ACCESSIBILITY_ID

    def progress_bar_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.PROGRESS_BAR_ACCESSIBILITY_ID

    def hide_controls_timeout(self):
        return DEFAULT_HIDE_CONTROLS_TIMEOUT

    def get_screen_id(self):
        return 'jw_player_screen'


class ApplicasterPlayer(AppPlayerInterface):
    """
    Public Implementation
    """
    def play_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.PLAY_PAUSE_BUTTON_ACCESSIBILITY_ID

    def pause_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.PAUSE_BUTTON_ACCESSIBILITY_ID

    def rew_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.REW_BUTTON_ACCESSIBILITY_ID

    def ffwd_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.FFWD_BUTTON_ACCESSIBILITY_ID

    def close_button_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.CLOSE_BUTTON_ACCESSIBILITY_ID

    def progress_bar_accessibility_identifier(self):
        return PlayerDefaultAccessibilityIdentifiers.PROGRESS_BAR_ACCESSIBILITY_ID

    def hide_controls_timeout(self):
        return DEFAULT_HIDE_CONTROLS_TIMEOUT

    def get_screen_id(self):
        return 'applicaster_player'


class FeatureAppPlayer(PlayerScreen):
    """
    Public Implementation
    """
    def hide_controls(self):
        PRINT('     Start hiding player controls controls')
        self.test.driver.wait(self.selected_player_.hide_controls_timeout())
        PRINT('     Finished hiding player controls controls')

    def select_applicaster_player(self):
        self.selected_player_ = self.applicaster_player_

    def select_jw_player(self):
        self.selected_player_ = self.jw_player_

    def get_screen_id(self):
        return self.selected_player_.get_screen_id()

    def press_play_button(self):
        self.__press_controls_button__(self.selected_player_.play_button_accessibility_identifier())

    def press_pause_button(self):
        self.__press_controls_button__(self.selected_player_.pause_button_accessibility_identifier())

    def press_rew_button(self):
        self.__press_controls_button__(self.selected_player_.rew_button_accessibility_identifier())

    def press_ffwd_button(self):
        self.__press_controls_button__(self.selected_player_.ffwd_button_accessibility_identifier())

    def press_close_button(self):
        self.__press_controls_button__(self.selected_player_.close_button_accessibility_identifier())

    def press_progress_bar(self, end_offset):
        self.show_controls()
        element = self.test.driver.find_element_by_accessibility_id(
            self.selected_player_.progress_bar_accessibility_identifier(),
            retries=2
        )
        print(element)
        print(dir(element))

    def __init__(self, test):
        self.test = test
        self.applicaster_player_ = ApplicasterPlayer(self.test.driver)
        self.jw_player_ = JwPlayer(self.test.driver)
        self.selected_player_ = self.applicaster_player_
        PlayerScreen.__init__(self, test)

    def __press_controls_button__(self, accessibility_identifier):
        self.show_controls()
        self.test.driver.find_element_by_accessibility_id(accessibility_identifier, retries=2).click()

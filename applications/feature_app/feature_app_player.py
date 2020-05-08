
from src.generic_building_blocks.player_screen import PlayerScreen
from src.global_defines import PlatformType
from src.configuration.configuration import Configuration

"""
Global Defines
"""
DEFAULT_HIDE_CONTROLS_TIMEOUT = 5
SHOW_CONTROLS_ANIMATION_DURATION = 0.4


class AppPlayerInterface(object):
    """
    Public Implementation
    """
    def hide_controls_timeout(self): raise NotImplementedError
    def get_screen_id(self): raise NotImplementedError
    def play_pause_button_accessibility_identifier(self): raise NotImplementedError
    def rew_button_accessibility_identifier(self): raise NotImplementedError
    def ffwd_button_accessibility_identifier(self):raise NotImplementedError

    """
    Private Implementation
    """
    def __init__(self, driver):
        self.driver = driver


class JwPlayer(AppPlayerInterface):
    PLAY_PAUSE_BUTTON_ACCESSIBILITY_ID = 'exo_play_pause'
    REW_BUTTON_ACCESSIBILITY_ID = 'exo_rew'
    FFWD_BUTTON_ACCESSIBILITY_ID = 'exo_ffwd'
    
    """
    Public Implementation
    """
    def play_pause_button_accessibility_identifier(self):
        return self.PLAY_PAUSE_BUTTON_ACCESSIBILITY_ID

    def rew_button_accessibility_identifier(self):
        return self.REW_BUTTON_ACCESSIBILITY_ID

    def ffwd_button_accessibility_identifier(self):
        return self.FFWD_BUTTON_ACCESSIBILITY_ID

    def hide_controls_timeout(self):
        return DEFAULT_HIDE_CONTROLS_TIMEOUT

    def get_screen_id(self):
        return 'jw_player_screen'


class ApplicasterPlayer(AppPlayerInterface):
    PLAY_PAUSE_BUTTON_ACCESSIBILITY_ID = 'com.featureappqbmobile:id/exo_play_pause'
    REW_BUTTON_ACCESSIBILITY_ID = 'exo_rew'
    FFWD_BUTTON_ACCESSIBILITY_ID = 'exo_ffwd'

    """
    Public Implementation
    """
    def play_pause_button_accessibility_identifier(self):
        return self.PLAY_PAUSE_BUTTON_ACCESSIBILITY_ID

    def rew_button_accessibility_identifier(self):
        return self.REW_BUTTON_ACCESSIBILITY_ID

    def ffwd_button_accessibility_identifier(self):
        return self.FFWD_BUTTON_ACCESSIBILITY_ID

    def hide_controls_timeout(self):
        return DEFAULT_HIDE_CONTROLS_TIMEOUT

    def get_screen_id(self):
        return 'applicaster_player'


class FeatureAppPlayer(PlayerScreen):
    """
    Public Implementation
    """
    def hide_controls(self):
        self.test.driver.press_screen_centre()
        self.test.driver.wait(self.selected_player_.hide_controls_timeout())

    def select_applicaster_player(self):
        self.selected_player_ = self.applicaster_player_

    def select_jw_player(self):
        self.selected_player_ = self.jw_player_

    def get_screen_id(self):
        return self.selected_player_.get_screen_id()

    def press_play_pause_button(self):
        self.show_controls()
        self.test.driver.find_element_by_id(self.selected_player_.play_pause_button_accessibility_identifier()).click()

    def press_rew_button(self):
        self.show_controls()
        self.test.driver.find_element_by_id(self.selected_player_.rew_button_accessibility_identifier()).click()

    def press_ffwd_button(self):
        self.show_controls()
        self.test.driver.find_element_by_id(self.selected_player_.ffwd_button_accessibility_identifier()).click()

    """
    Private Implementation 
    """
    def __init__(self, test):
        self.test = test
        self.applicaster_player_ = ApplicasterPlayer(self.test.driver)
        self.jw_player_ = JwPlayer(self.test.driver)
        self.selected_player_ = self.applicaster_player_
        PlayerScreen.__init__(self, test)

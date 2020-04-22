
from src.generic_building_blocks.player_screen import PlayerScreen

DEFAULT_HIDE_CONTROLS_TIMEOUT = 5
SHOW_CONTROLS_ANIMATION_DURATION = 0.4


class AppPlayerInterface(object):
    """
    Public Implementation
    """
    def hide_controls(self): raise NotImplementedError
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
    def hide_controls(self):
        self.driver.wait(DEFAULT_HIDE_CONTROLS_TIMEOUT)

    def get_screen_id(self):
        return 'jw_player_screen'


class ApplicasterPlayer(AppPlayerInterface):
    """
    Public Implementation
    """
    def hide_controls(self):
        self.driver.wait(DEFAULT_HIDE_CONTROLS_TIMEOUT)

    def get_screen_id(self):
        return 'applicaster_player'


class FeatureAppScreen(PlayerScreen):
    """
    Public Implementation
    """
    def hide_controls(self):
        self.selected_player_.hide_controls()

    def select_applicaster_player(self):
        self.selected_player_ = self.applicaster_player_

    def select_jw_player(self):
        self.selected_player_ = self.jw_player_

    def get_screen_id(self):
        return self.selected_player_.get_screen_id()

    """
    Private Implementation 
    """
    def __init__(self, test):
        self.test = test
        self.applicaster_player_ = ApplicasterPlayer(self.test.driver)
        self.jw_player_ = JwPlayer(self.test.driver)
        self.selected_player_ = self.applicaster_player_
        PlayerScreen.__init__(self, test)

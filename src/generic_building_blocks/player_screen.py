
from src.generic_building_blocks.generic_screen import GenericScreen
from src.global_defines import ScreenType
from src.utils.logger import Logger
from src.global_defines import ScreenUiState
from src.global_defines import PlatformType
from src.base_test import PRINT, Configuration

'''
Global Defines
'''
ERROR_VERIFY_STREAM_IS_PLAYING = 'Failed verifying that the streaming is playing correctly'
ERROR_VERIFY_STREAM_IS_NOT_PLAYING = 'Failed verifying that the streaming is not playing correctly'
DEFAULT_HIDE_CONTROLS_TIMEOUT = 5


class PlayerDefaultAccessibilityIdentifiers:
    PLAY_BUTTON_ACCESSIBILITY_ID = 'controls_play_button'
    PAUSE_BUTTON_ACCESSIBILITY_ID = 'controls_pause_button'
    REW_BUTTON_ACCESSIBILITY_ID = 'controls_rewind_button'
    FFWD_BUTTON_ACCESSIBILITY_ID = 'controls_forward_button'
    CLOSE_BUTTON_ACCESSIBILITY_ID = 'controls_close_button'
    PROGRESS_BAR_ACCESSIBILITY_ID = 'controls_progress_bar'


class PlayerScreen(GenericScreen):
    """
    Public Implementation
    """
    def press_play_button(self): raise NotImplementedError
    def press_pause_button(self): raise NotImplementedError
    def press_rew_button(self): raise NotImplementedError
    def press_ffwd_button(self): raise NotImplementedError
    def press_close_button(self): raise NotImplementedError
    def press_progress_bar(self, end_offset): raise NotImplementedError
    def hide_controls(self): raise NotImplementedError

    def navigate(self): pass

    def close(self):
        if Configuration.get_instance().platform_type() not in (PlatformType.ANDROID, PlatformType.ANDROID_TV):
            # in case the player is not android
            raise NotImplementedError
            
        self.test.driver.back()

    def get_screen_type(self):
        return ScreenType.STANDALONE_SCREEN

    def screen_UI_state(self, sampling_count=4, measure_delay=1):
        sampling_array = []
        for i in range(sampling_count):
            snapshot_before = self.test.driver.get_screenshot_as_base64()
            self.test.driver.wait(measure_delay)
            snapshot_after = self.test.driver.get_screenshot_as_base64()
            state = ScreenUiState.STATIC if snapshot_before == snapshot_after else ScreenUiState.DYNAMIC
            sampling_array.append(state)

        counter = 0
        for state in sampling_array:
            if state == ScreenUiState.STATIC:
                counter += 1

        return ScreenUiState.STATIC if counter >= 2 else ScreenUiState.DYNAMIC

    def verify_stream_is_playing(self, retries=1):
        self.hide_controls()

        ui_status = ScreenUiState.STATIC
        for i in range(retries):
            ui_status = self.screen_UI_state()
            if ui_status == ScreenUiState.DYNAMIC:
                break
        Logger.get_instance().log_assert(ui_status == ScreenUiState.DYNAMIC, ERROR_VERIFY_STREAM_IS_PLAYING)

    def verify_stream_is_not_playing(self):
        self.hide_controls()
        ui_status = self.screen_UI_state()
        Logger.get_instance().log_assert(ui_status == ScreenUiState.STATIC, ERROR_VERIFY_STREAM_IS_NOT_PLAYING)
    
    def show_controls(self):
        PRINT('     Start showing player controls')
        self.hide_controls()
        self.test.driver.press_screen_centre()
        PRINT('     Finished showing player controls')

    """
    Private Implementation
    """
    def __init__(self, test):
        GenericScreen.__init__(self, test)

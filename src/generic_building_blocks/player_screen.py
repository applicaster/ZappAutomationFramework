
from src.generic_building_blocks.generic_screen import GenericScreen
from src.global_defines import ScreenType
from src.utils.logger import Logger
from src.global_defines import ScreenUiState

'''
Global Defines
'''
ERROR_VERIFY_STREAM_IS_PLAYING = 'Test failed to verify that the streaming is playing'
ERROR_VERIFY_STREAM_IS_NOT_PLAYING = 'Test failed to verify that the streaming is not playing'


class PlayerScreen(GenericScreen):
    """
    Public Implementation
    """
    def hide_controls(self): raise NotImplementedError

    def navigate(self): pass

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

    """
    Private Implementation
    """
    def __init__(self, test):
        GenericScreen.__init__(self, test)

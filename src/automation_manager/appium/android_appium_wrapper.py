
from src.utils.logger import Logger
from src.global_defines import RemoteControlKeys
from src.automation_manager.appium.base_appium_wrapper import BaseAppiumWrapper
from src.automation_manager.appium.base_appium_wrapper import FINDING_ELEMENT_BY_TEXT


class AndroidRemoteControlKeyCodes:
    UP = 19
    DOWN = 20
    RIGHT = 22
    LEFT = 21
    ENTER = 23
    BACK = 4


class AndroidAppiumWrapper(BaseAppiumWrapper):
    """
    Public Implementation
    """
    def find_element_by_text(self, text, retries=1):
        for i in range(retries):
            try:
                text_views_widgets = self.driver_.find_elements_by_class_name('android.widget.TextView')
                for view in text_views_widgets:
                    if view.text == text:
                        return view

                button_views_widgets = self.driver_.find_elements_by_class_name('android.widget.Button')
                for button in button_views_widgets:
                    if button.text == text:
                        return button

            except Exception as exception:
                Logger.get_instance().warning(self, "find_element_by_text", FINDING_ELEMENT_BY_TEXT % str(text))

            self.wait(1)

        return None

    def get_device_log(self):
        """
        Gets the log for a given log type
        """
        return self.driver_.get_log('logcat')

    '''
    Private Implementation
    '''
    def __send_key__(self, key_code):
        self.driver_.press_keycode(key_code)

    def __convert_key_code__(self, key_code):
        if key_code == RemoteControlKeys.UP:
            return AndroidRemoteControlKeyCodes.UP

        if key_code == RemoteControlKeys.DOWN:
            return AndroidRemoteControlKeyCodes.DOWN

        if key_code == RemoteControlKeys.LEFT:
            return AndroidRemoteControlKeyCodes.LEFT

        if key_code == RemoteControlKeys.RIGHT:
            return AndroidRemoteControlKeyCodes.RIGHT

        if key_code == RemoteControlKeys.ENTER:
            return AndroidRemoteControlKeyCodes.ENTER

        if key_code == RemoteControlKeys.BACK:
            return AndroidRemoteControlKeyCodes.BACK

        return key_code

    """
    Private Implementation
    """
    def __init__(self, desired_capabilities, appium_server_host):
        BaseAppiumWrapper.__init__(self, desired_capabilities, appium_server_host)

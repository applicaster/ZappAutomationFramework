
from src.utils.logger import Logger
from src.utils.print import PRINT

"""
Global Defines
"""
ERROR_VERIFY_TEXT_FOUND_ON_SCREEN = 'Test failed to verify text string "%s" on screen'
ERROR_VERIFY_ACCESSIBILITY_ID_FOUND_ON_SCREEN = 'Test failed to verify accessibility id "%s" on screen'


class Verifier(object):
    """
    Public Implementation
    """
    def verify_elements_on_screen_by_text(self, texts_array, retries=1):
        self.__verify_elements_on_screen__(texts_array, veri_type='text', retries=retries)

    def verify_elements_on_screen_by_accessibility_identifier(self, accessibility_ids_array, retries=1):
        self.__verify_elements_on_screen__(accessibility_ids_array, veri_type='id', retries=retries)

    """
    Private Implementation 
    """
    def __verify_elements_on_screen__(self, items_array, veri_type='text', retries=1):
        if isinstance(items_array, str):
            items_array = [items_array]

        for item in items_array:
            if veri_type == 'text':
                element = self.driver.find_element_by_text(item, retries=retries)
                Logger.get_instance().log_assert(element is not None, ERROR_VERIFY_TEXT_FOUND_ON_SCREEN % str(item))
            else:
                element = self.driver.find_element_by_accessibility_id(item, retries=retries)
                Logger.get_instance().log_assert(element is not None, ERROR_VERIFY_ACCESSIBILITY_ID_FOUND_ON_SCREEN % str(item))
            PRINT('     Item "%s" found by %s correctly on the screen' % (item, veri_type))

    def __init__(self, driver):
        self.driver = driver

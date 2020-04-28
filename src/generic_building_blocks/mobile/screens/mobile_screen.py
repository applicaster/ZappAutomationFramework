
from src.utils.print import PRINT
from src.global_defines import Direction, SwipeArea
from src.generic_building_blocks.generic_screen import GenericScreen, DERIVED_CLASS_MISSING_IMPLEMENTATION


class MobileScreen(GenericScreen):
    def __init__(self, test):
        GenericScreen.__init__(self, test)

    def get_screen_id(self):
        PRINT(DERIVED_CLASS_MISSING_IMPLEMENTATION % ('MobileScreen', 'get_screen_id()'), 'red')
        raise NotImplementedError

    def swipe(self, distance=None, direction=Direction.UP, area=SwipeArea.CENTER, rect=None):
        """
        :param distance: The range you want to perform the swipe, if value is None swipe will be 1/3 of the screen
        :param direction: Can be UP, DOWN, LEFT, RIGHT
        :param area: Screen is divided to 3 swipe sections, TOP is the first 1/3 section of the screens, CENTER is
                     center point of the screen and BOTTOM is last 1/3 section of the screen
        :param rect: The rect where the swipe is being performed on
        """
        if rect is None:
            rect = self.test.driver.get_window_rect()

        VERTICAL_SWIPE = direction == Direction.UP or direction == Direction.DOWN
        HORIZONTAL_SWIPE = direction == Direction.LEFT or direction == Direction.RIGHT

        """
        Calculate the swipe start point
        """
        section_size = rect['height'] / 3
        start_x = rect['x'] + (rect['width'] / 2)
        if area == SwipeArea.TOP:
            start_y = rect['y'] + (section_size / 2)

        elif area == SwipeArea.CENTER:
            start_y = rect['y'] + (rect['height'] / 2)

        elif area == SwipeArea.BOTTOM:
            start_y = rect['y'] + (section_size * 2.5)

        """
        Calculate the swipe end point
        """
        if distance is None and VERTICAL_SWIPE:
            distance = rect['height'] / 3

        elif distance is None and HORIZONTAL_SWIPE:
            distance = rect['width'] / 3

        if direction == Direction.UP or direction == Direction.LEFT:
            distance *= -1

        end_y = start_y if HORIZONTAL_SWIPE else start_y + distance
        end_x = start_x if VERTICAL_SWIPE else start_x + distance

        self.test.driver.swipe_by_coordinates(start_x, start_y, end_x, end_y)

    def dismiss_react_native_yellow_console_box(self):
        self.test.driver.find_element_by_text('Dismiss All', retries=5).click()

    def search_horizontally_for_item_by_text(self, text, distance, direction, area):
        """
        :param text: The text in element we are looking for
        :param distance: The range you want to perform the swipe, if value is None swipe will be 1/3 of the screen
        :param direction: Can be LEFT, RIGHT
        :param area: Screen is divided to 3 swipe sections, TOP is the first 1/3 section of the screens, CENTER is
                     center point of the screen and BOTTOM is last 1/3 section of the screen
        """
        element = None
        counter = 0
        while counter < 35:
            element = self.test.driver.find_element_by_text(text)
            if element is not None:
                break
            self.swipe(distance=distance, direction=direction, area=area)
            counter += 1
        return element

    def search_for_item_by_text(self, text, scroll_to_top=False):
        """
        The following function scroll and search for element on screens by text
        :param text: The text in element we are looking for
        :param scroll_to_top: define if you want to scroll to top of the screen before start the search
        :return: the element if found None if not
        """
        return self.__search_by_type__('text', text, scroll_top=scroll_to_top)

    def search_for_item_by_id(self, accessibility_id, scroll_to_top=False):
        """
        The following function scroll and search for element on screens by id
        :param accessibility_id: The element identifier we are looking for
        :param scroll_to_top: define if you want to scroll to top of the screen before start the search
        :return: the element if found None if not
        """
        return self.__search_by_type__('id', accessibility_id, scroll_top=scroll_to_top)

    """
    Private Implementation 
    """
    def __search_by_type__(self, access_type, value, scroll_top=False):
        if scroll_top is True:
            before = self.test.driver.get_screenshot_as_base64()
            while True:
                self.swipe(direction=Direction.DOWN)
                self.test.driver.wait(1)
                after = self.test.driver.get_screenshot_as_base64()

                if before == after:
                    break

                before = after

        # scroll down and search
        element = None
        before = self.test.driver.get_screenshot_as_base64()
        while True:

            if access_type == 'text':
                element = self.test.driver.find_element_by_text(value, retries=5)

            elif access_type == 'id':
                element = self.test.driver.find_element_by_accessibility_id(value, retries=5)

            if element:
                break

            self.swipe()
            self.test.driver.wait(1)
            after = self.test.driver.get_screenshot_as_base64()
            if before == after:
                break

            before = after

        return element

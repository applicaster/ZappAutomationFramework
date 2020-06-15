
import pytest

from src.automation_manager.automation_manager import automation_driver
from src.utils.print import PRINT
from src.base_test import BaseTest


@pytest.mark.qb_android_mobile
# @pytest.mark.qb_ios_mobile
@pytest.mark.usefixtures('automation_driver')
class LaunchToHomeTest(BaseTest):
    def test_launch_to_home(self):
        PRINT('Test, inside test body')
        PRINT('Test steps finished running successfully', 'yellow', 'on_blue', ['bold'])

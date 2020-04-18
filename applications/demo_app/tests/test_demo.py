
import pytest
from src.base_test import BaseTest, PRINT
from src.automation_manager.automation_manager import automation_driver


@pytest.mark.usefixtures('automation_driver')
class DemoTest(BaseTest):
    def test_demo_test_1(self):
        PRINT('inside FirstTest test_demo_test_1')

    def test_demo_test_2(self):
        PRINT('inside FirstTest test_demo_test_2')




class AutomationDriver(object):
    def connect(self, retries=1): raise NotImplementedError
    def disconnect(self): raise NotImplementedError
    def find_element_by_text(self, text, retries=1): raise NotImplementedError
    def find_element_by_accessibility_id(self, find_element_by_accessibility_id, retries=1): raise NotImplementedError
    def wait(self, seconds): raise NotImplementedError
    def activate_app(self, bundle_id=None, app_package=None): raise NotImplementedError
    def terminate_app(self): raise NotImplementedError
    def get_device_log(self): raise NotImplementedError

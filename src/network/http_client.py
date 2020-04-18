
from time import sleep

import requests

from src.utils.logger import Logger

'''
Global Defines
'''
REQUEST_TIMEOUT = 5
RETRIES = 1


class HttpClient(object):

    def do_get(self, url, params=None, retries=RETRIES):
        response = None

        for i in range(retries):
            try:
                response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
                if response.status_code == requests.codes.ok:
                    break
                sleep(0.5)

            except Exception as exception:
                Logger.get_instance().error(self, "do_get", "Failed performing GET request for url: %s" % url)
                Logger.get_instance().error(self, "do_get", exception)

        return response

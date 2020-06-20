import logging
import time
import botocore
import urllib3

log = logging.getLogger(__name__)

BACKOFF = .25
MAX_RETRIES = 5


class Utils:

    @staticmethod
    def retry(function):
        """
        Decorator that supports automatic retries if connectivity issues are detected with boto or urllib operations
        """

        def inner(self, *args, **kwargs):
            retries = 0
            while True:
                try:
                    return function(self, *args, **kwargs)
                except (botocore.exceptions.EndpointConnectionError, urllib3.exceptions.NewConnectionError) as e:
                    log.error(e)
                    if retries > MAX_RETRIES:
                        raise e

                    retries += 1
                    time.sleep(retries * BACKOFF)

        return inner
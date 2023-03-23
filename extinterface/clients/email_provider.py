from abc import ABCMeta, abstractmethod


class EmailProvider(object, metaclass=ABCMeta):
    """Abstract class to be inherited and
        extended by the individual email providers"""

    def __init__(self):
        pass

    @abstractmethod
    def process_request(self, request):
        """this method will process
        the request for individual email provider"""

        pass

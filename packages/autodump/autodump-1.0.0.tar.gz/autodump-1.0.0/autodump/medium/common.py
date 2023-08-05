from abc import ABC, abstractmethod


class Medium(ABC):

    def __init__(self, param):
        self._param = param
        self._check_param()

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def _check_param(self):
        pass

    @abstractmethod
    def cache(self):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def persist(self):
        pass

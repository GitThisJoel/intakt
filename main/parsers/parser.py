import abc
from abc import abstractmethod

# TODO: improve this class
class Parser(metaclass=abc.ABCMeta):
    @staticmethod
    @abstractmethod
    def __str__(*args, **kwargs):
        ...

    @staticmethod
    @abstractmethod
    def parse(data, time_delta, *args, **kwargs):
        ...

    @staticmethod
    @abstractmethod
    def get_data(start_time, end_time, *args, **kwargs):
        ...

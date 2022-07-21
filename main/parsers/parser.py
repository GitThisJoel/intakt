import abc

# TODO: improve this class
class Parser(metaclass=abc.ABCMeta):
    @abc.metaclass
    def parse(data, time_delta, *args, **kwargs):
        ...

    @abc.metaclass
    def get_data(data, *args, **kwargs):
        ...

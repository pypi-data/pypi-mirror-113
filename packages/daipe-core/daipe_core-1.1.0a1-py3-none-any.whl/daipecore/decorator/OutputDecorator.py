from injecta.container.ContainerInterface import ContainerInterface
from daipecore.decorator.BaseDecorator import BaseDecorator
from daipecore.decorator.InputDecorator import InputDecorator
from daipecore.decorator.DecoratedFunctionInjector import DecoratedFunctionInjector


class OutputDecorator(BaseDecorator, metaclass=DecoratedFunctionInjector):

    _input_decorator: InputDecorator

    def set_input_decorator(self, input_decorator: InputDecorator):
        self._input_decorator = input_decorator

    def process_result(self, result, container: ContainerInterface):
        pass

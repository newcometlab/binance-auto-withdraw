""" Abstract wallet """

from abc import ABC, abstractmethod

from client.client import Client
from logger.app_logger import AppLogger


class AbstractWallet(ABC):
    """ Abstract wallet """

    def __init__(self):
        self.client = Client().get()
        self.logger = AppLogger().get()

    @abstractmethod
    def get_balance(self):
        """ Implement to retrieve balance """

    @abstractmethod
    def print_balance(self):
        """ Implement to print balance """

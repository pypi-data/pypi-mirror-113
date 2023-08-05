from abc import *


class Preprocessor(metaclass=ABCMeta):

    @abstractmethod
    def load_original_data(self, **kwargs):
        # this method should load the original data
        pass

    @abstractmethod
    def save_processed_data(self, **kwargs):
        # this method should save the processed data
        pass

    @abstractmethod
    def process(self, **kwargs):
        # this method should take the original data and process and return the processed data or save it
        pass

    @abstractmethod
    def split_dataset(self, **kwargs):
        # this should split the dataset for training, validation, and testing
        pass

    @abstractmethod
    def __repr__(self):
        # this should explain how the data is processed before training
        pass

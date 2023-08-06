from abc import *

TRAINING_MODE = 1
INFERENCE_MODE = 2


class AbstractProcessor:
    representation = ''


class Preprocessor(AbstractProcessor, metaclass=ABCMeta):

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


class ModelDesigner(AbstractProcessor):
    model = None

    def __init__(self, **kwargs):
        self.status = kwargs.get("status", TRAINING_MODE)

    @abstractmethod
    def build_model(self, **kwargs):
        # this method should have model structure
        pass

    def get_model(self, **kwargs):
        if self.model is None:
            self.model = self.build_model(**kwargs)
            return self.model
        else:
            return self.model

    @abstractmethod
    def loss_function(self, *args, **kwargs):
        # this method should be the loss function
        pass

    @abstractmethod
    def load_weight(self, **kwargs):
        # this method should return the model with the specific weight
        pass

    @abstractmethod
    def save_weight(self, **kwargs):
        # this method should save the weight that the model already has
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Trainer(AbstractProcessor):

    @abstractmethod
    def load_training_dataset(self, **kwargs):
        pass

    @abstractmethod
    def load_pretrained_weight(self, **kwargs):
        pass

    @abstractmethod
    def load_training_recipe(self, **kwargs):
        pass

    @abstractmethod
    def train(self, **kwargs):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Evaluator(AbstractProcessor):
    @abstractmethod
    def __repr__(self):
        pass

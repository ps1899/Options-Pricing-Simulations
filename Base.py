from enum import Enum
from abc import ABC, abstractclassmethod

class OptionType(Enum):
    CallOption = 'Call Option'
    PutOption = 'Put Option'

class OptionPricingModel(ABC):

    @abstractclassmethod
    def calculate_call_option_price():
        pass
    
    @abstractclassmethod
    def calculate_put_option_price():
        pass

    def calculate_option_price(self, option_type):
        if(option_type == OptionType.CallOption.value):
            return self.calculate_call_option_price()
        elif(option_type == OptionType.PutOption.value):
            return self.calculate_put_option_price()
        else:
            return -1
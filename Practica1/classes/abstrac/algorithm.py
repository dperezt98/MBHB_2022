from abc import ABC, abstractmethod

class Algorithm(ABC):
    """
    Algoritmo que puede ser ejecutado mediante la funcion run()
    """
    
    @abstractmethod
    def movement_operator():
        pass

    @abstractmethod
    def run():
        pass


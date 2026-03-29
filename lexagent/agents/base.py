"""Base agent abstractions."""

from abc import ABC, abstractmethod #Lets you create abstract base classes.
from typing import Any


# abstract base class : is meant to be a blueprint for other classes.
class BaseAgent(ABC):
    """Simple abstract base class for all agents."""

    name: str

    @abstractmethod
    def run(self, payload: Any) -> Any:    # payload : Any means payload can be anything int, string, etc. and output is also Any
        raise NotImplementedError
    # run function is compulsary to implement in any subclass of BaseAgent. If not implemented, it will raise NotImplementedError when called.       

from abc import ABC, abstractmethod


class IMaterialObject(ABC):
    @abstractmethod
    def get_area(self):
        pass

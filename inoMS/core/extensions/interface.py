from abc import abstractmethod, ABC


class ExtensionInterface(ABC):
    @abstractmethod
    def install_extension(self) -> None:
        ...

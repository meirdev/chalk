from typing import Annotated, Generic, TypeVar


class ValueRange:
    def __init__(self, min: int, max: int) -> None:
        self.min = min
        self.max = max


u8 = Annotated[int, ValueRange(0, 256)]


T = TypeVar("T")


class Symbol(Generic[T]):
    def __init__(self, obj: T) -> None:
        self.obj = obj

    def get(self) -> T:
        return self.obj

    def set(self, obj: T) -> None:
        self.obj = obj

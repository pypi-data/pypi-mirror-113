# Custom exceptions for dslq

class RangeError(Exception):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"Invalid value {self.value} for range"


class INError(Exception):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"IN operatator must be a tuple not {type(self.value)}"

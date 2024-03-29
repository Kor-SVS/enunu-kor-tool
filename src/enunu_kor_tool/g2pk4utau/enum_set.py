from enum import Enum, Flag, auto, unique


@unique
class VerboseMode(Flag):
    NONE = auto()
    PARAMETER = auto()
    INPUT = auto()
    PREPHN = auto()
    G2PK = auto()
    G2P4UTAU = auto()
    OUTPUT = auto()
    INPUT_OUTPUT = INPUT | OUTPUT
    PROGRESS = PREPHN | G2PK | G2P4UTAU
    ALL = PARAMETER | INPUT_OUTPUT | PROGRESS

    def is_flag(self, item) -> bool:
        return (self.value & item.value) != 0

    def __contains__(self, item) -> bool:
        return (self.value & item.value) == item.value


@unique
class CacheMode(Enum):
    NONE = auto()
    MEMORY = auto()
    FILE = auto()

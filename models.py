"""Main models for the Library."""

import enum
from dataclasses import asdict, dataclass, field


class BookStatus(str, enum.Enum):
    """Book status enumerate."""

    AVAILABLE = "в наличии"
    BORROWED = "выдана"


@dataclass
class Book:
    """Book model."""

    id: str
    title: str
    author: str
    year: int
    status: str = field(default=BookStatus.AVAILABLE)

    def __str__(self) -> str:
        """Return a string representation of the Book object."""
        return (
            f'<{self.id}>; Книга "{self.title}": автор {self.author}, '
            f"год {self.year}, сейчас {self.status}"
        )

    def __post_init__(self) -> None | ValueError:
        """Do additional processing of instance variables here."""
        if not isinstance(self.year, int):
            self.year = int(self.year)
        if not isinstance(self.id, str):
            self.id = str(self.id)

    @property
    def as_dict(self) -> dict:
        """Return a dictionary representation of the Book object."""
        return asdict(self)

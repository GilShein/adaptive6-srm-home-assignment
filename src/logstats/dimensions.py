from collections.abc import Callable
from dataclasses import dataclass

from logstats.parse import Record

UNKNOWN = "Unknown"


@dataclass(frozen=True, slots=True)
class Agent:
    os: str
    browser: str


@dataclass(frozen=True, slots=True)
class Dimension:
    name: str
    label: Callable[[Record], str]


def default_dimensions(
    country_of: Callable[[str], str], agent_of: Callable[[str], Agent]
) -> list[Dimension]:
    return [
        Dimension("Country", lambda record: country_of(record.ip)),
        Dimension("OS", lambda record: agent_of(record.ua).os),
        Dimension("Browser", lambda record: agent_of(record.ua).browser),
    ]

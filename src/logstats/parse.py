import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

INSIDE_QUOTES = r'[^"\\]*(?:\\.[^"\\]*)*'
LINE = re.compile(
    rf'^(?P<ip>\S+) \S+ \S+ \[[^\]]*\] "{INSIDE_QUOTES}" (?P<status>\S+) (?P<size>\S+) '
    rf'"{INSIDE_QUOTES}" "(?P<ua>{INSIDE_QUOTES})"$'
)


@dataclass(frozen=True, slots=True)
class Record:
    ip: str
    status: str
    size: str
    ua: str


def parse(line: str) -> Record | None:
    match = LINE.match(line.rstrip("\r\n"))
    if match is None:
        return None
    return Record(
        ip=match["ip"],
        status=match["status"],
        size=match["size"],
        ua=match["ua"],
    )


def read_records(lines: Iterable[str]) -> Iterator[Record | None]:
    for line in lines:
        if line.strip():
            yield parse(line)

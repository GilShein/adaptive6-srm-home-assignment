from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Self

from logstats.dimensions import UNKNOWN, Dimension
from logstats.parse import Record


@dataclass(frozen=True, slots=True)
class Report:
    total: int = 0
    unparsed: int = 0
    counts: dict[str, Counter[str]] = field(default_factory=dict)

    def __add__(self, other: Self) -> Self:
        names = [
            *self.counts,
            *(name for name in other.counts if name not in self.counts),
        ]
        return type(self)(
            total=self.total + other.total,
            unparsed=self.unparsed + other.unparsed,
            counts={
                name: self.counts.get(name, Counter[str]())
                + other.counts.get(name, Counter[str]())
                for name in names
            },
        )


def aggregate(records: Iterable[Record | None], dimensions: list[Dimension]) -> Report:
    counts = {dimension.name: Counter[str]() for dimension in dimensions}
    total = unparsed = 0
    for record in records:
        total += 1
        if record is None:
            unparsed += 1
            for dimension in dimensions:
                counts[dimension.name][UNKNOWN] += 1
            continue
        for dimension in dimensions:
            counts[dimension.name][dimension.label(record)] += 1
    return Report(total=total, unparsed=unparsed, counts=counts)

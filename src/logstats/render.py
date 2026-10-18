from decimal import ROUND_HALF_UP, Decimal

from logstats.report import Report

TWO_PLACES = Decimal("0.01")


def percent(count: int, total: int) -> str:
    share = Decimal(100 * count) / total
    return f"{share.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)}%"


def by_frequency(row: tuple[str, int]) -> tuple[int, str]:
    label, count = row
    return -count, label


def render_text(report: Report) -> str:
    lines = []
    for name, counts in report.counts.items():
        lines.append(f"{name}:")
        rows = sorted(counts.items(), key=by_frequency)
        lines.extend(f"{label} {percent(count, report.total)}" for label, count in rows)
    return "\n".join(lines) + "\n"

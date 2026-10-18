from collections import Counter

import pytest
from support import (
    CHROME_ON_MAC_LINE,
    DASH_AGENT_LINE,
    FIREFOX_ON_UBUNTU_LINE,
    GARBAGE_LINE,
    GOOGLEBOT_LINE,
    TRUNCATED_AGENT_LINE,
    fake_dimensions,
)

from logstats.dimensions import Dimension
from logstats.parse import read_records
from logstats.report import Report, aggregate


def test_three_lines_are_counted_per_dimension() -> None:
    report = aggregate(
        read_records([CHROME_ON_MAC_LINE, DASH_AGENT_LINE, FIREFOX_ON_UBUNTU_LINE]),
        fake_dimensions(),
    )

    assert report == Report(
        total=3,
        unparsed=0,
        counts={
            "Country": Counter({"Russia": 1, "Guatemala": 1, "United States": 1}),
            "OS": Counter({"Mac OS X": 1, "Unknown": 1, "Ubuntu": 1}),
            "Browser": Counter({"Chrome": 1, "Unknown": 1, "Firefox": 1}),
        },
    )


@pytest.mark.parametrize(
    "line", [GARBAGE_LINE, TRUNCATED_AGENT_LINE], ids=["garbage", "truncated_agent"]
)
def test_line_that_does_not_parse_counts_as_unknown_in_every_dimension(
    line: str,
) -> None:
    report = aggregate(read_records([line]), fake_dimensions())

    assert (report.total, report.unparsed) == (1, 1)
    assert {name: counts["Unknown"] for name, counts in report.counts.items()} == {
        "Country": 1,
        "OS": 1,
        "Browser": 1,
    }


def test_blank_lines_are_not_requests() -> None:
    report = aggregate(read_records([CHROME_ON_MAC_LINE, "\n", ""]), fake_dimensions())

    assert report.total == 1


def test_reports_of_two_chunks_add_up_to_one_pass() -> None:
    lines = [
        CHROME_ON_MAC_LINE,
        DASH_AGENT_LINE,
        FIREFOX_ON_UBUNTU_LINE,
        GARBAGE_LINE,
        TRUNCATED_AGENT_LINE,
    ]
    first = aggregate(read_records(lines[:2]), fake_dimensions())
    second = aggregate(read_records(lines[2:]), fake_dimensions())

    merged = sum([first, second], Report())

    assert merged == Report(
        total=5,
        unparsed=2,
        counts={
            "Country": Counter(
                {"Russia": 1, "Guatemala": 1, "United States": 1, "Unknown": 2}
            ),
            "OS": Counter({"Mac OS X": 1, "Ubuntu": 1, "Unknown": 3}),
            "Browser": Counter({"Chrome": 1, "Firefox": 1, "Unknown": 3}),
        },
    )


def test_status_dimension_needs_no_production_change() -> None:
    dimensions = [*fake_dimensions(), Dimension("Status", lambda record: record.status)]

    report = aggregate(
        read_records([CHROME_ON_MAC_LINE, DASH_AGENT_LINE, GARBAGE_LINE]), dimensions
    )

    assert report.counts["Status"] == {"200": 2, "Unknown": 1}


def test_records_filtered_before_aggregate_never_reach_the_dimensions() -> None:
    records = read_records([CHROME_ON_MAC_LINE, GOOGLEBOT_LINE, GARBAGE_LINE])
    humans = (
        record for record in records if record is None or "Googlebot" not in record.ua
    )

    report = aggregate(humans, fake_dimensions())

    assert (report.total, report.unparsed) == (2, 1)

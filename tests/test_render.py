from collections import Counter

from support import (
    CHROME_ON_MAC_LINE,
    DASH_AGENT_LINE,
    FIREFOX_ON_UBUNTU_LINE,
    fake_dimensions,
)

from logstats.parse import read_records
from logstats.render import render_text
from logstats.report import Report, aggregate


def test_three_lines_render_in_the_brief_layout() -> None:
    report = aggregate(
        read_records([CHROME_ON_MAC_LINE, DASH_AGENT_LINE, FIREFOX_ON_UBUNTU_LINE]),
        fake_dimensions(),
    )

    assert render_text(report) == (
        "Country:\n"
        "Guatemala 33.33%\n"
        "Russia 33.33%\n"
        "United States 33.33%\n"
        "OS:\n"
        "Mac OS X 33.33%\n"
        "Ubuntu 33.33%\n"
        "Unknown 33.33%\n"
        "Browser:\n"
        "Chrome 33.33%\n"
        "Firefox 33.33%\n"
        "Unknown 33.33%\n"
    )


def test_ties_order_by_label_code_point_and_unknown_keeps_its_rank() -> None:
    report = Report(
        total=6, counts={"OS": Counter({"b": 1, "a": 1, "Unknown": 3, "Z": 1})}
    )

    assert render_text(report) == "OS:\nUnknown 50.00%\nZ 16.67%\na 16.67%\nb 16.67%\n"


def test_percentages_round_half_up_on_exact_ties() -> None:
    report = Report(total=800, counts={"Browser": Counter({"Chrome": 799, "Lynx": 1})})

    assert render_text(report) == "Browser:\nChrome 99.88%\nLynx 0.13%\n"


def test_each_row_is_rounded_on_its_own() -> None:
    report = Report(total=3, counts={"Browser": Counter({"Chrome": 2, "Googlebot": 1})})

    assert render_text(report) == "Browser:\nChrome 66.67%\nGooglebot 33.33%\n"

import pytest
from support import (
    CHROME_ON_MAC_AGENT,
    CHROME_ON_MAC_LINE,
    DASH_AGENT_LINE,
    GARBAGE_LINE,
    TRUNCATED_AGENT_LINE,
)

from logstats.parse import Record, parse, read_records


def test_user_agent_is_the_last_quoted_field() -> None:
    assert parse(CHROME_ON_MAC_LINE) == Record(
        ip="83.149.9.216",
        status="200",
        size="203023",
        ua=CHROME_ON_MAC_AGENT,
    )


def test_line_missing_its_agent_closing_quote_does_not_parse() -> None:
    assert parse(TRUNCATED_AGENT_LINE) is None


def test_dash_agent_is_kept_as_written() -> None:
    record = parse(DASH_AGENT_LINE)

    assert record is not None
    assert record.ua == "-"


def test_garbage_line_does_not_parse() -> None:
    assert parse(GARBAGE_LINE) is None


def test_escaped_quote_in_the_agent_stays_part_of_the_agent() -> None:
    record = parse(
        '81.2.69.160 - - [17/May/2015:10:05:03 +0000] "GET / HTTP/1.1" 200 5 "-" '
        '"Mozilla/5.0 (say \\"hi\\")"\n'
    )

    assert record is not None
    assert record.ua == 'Mozilla/5.0 (say \\"hi\\")'


@pytest.mark.parametrize(
    "line",
    [
        '81.2.69.160 - - [17/May/2015:10:05:03 +0000] "GET /?q=\\"a\\" HTTP/1.1" 200 5 "-" "curl/7.0"\n',
        '81.2.69.160 - - [17/May/2015:10:05:03 +0000] "GET / HTTP/1.1" 200 5 "http://example.com/?q=\\"a\\"" "curl/7.0"\n',
    ],
    ids=["request", "referrer"],
)
def test_escaped_quote_in_an_earlier_field_does_not_break_the_line(line: str) -> None:
    record = parse(line)

    assert record is not None
    assert record.ua == "curl/7.0"


def test_blank_lines_are_not_records() -> None:
    records = list(read_records([CHROME_ON_MAC_LINE, "\n", "   \n", ""]))

    assert len(records) == 1


def test_line_that_does_not_parse_is_read_as_none() -> None:
    assert list(read_records([GARBAGE_LINE])) == [None]

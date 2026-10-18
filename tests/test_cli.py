import os
import subprocess
import sys
from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path

import geoip2.database
import pytest
from support import CHROME_ON_MAC_LINE, GARBAGE_LINE, TEST_DB, UK_CHROME_ON_MAC_LINE

REPO = Path(__file__).parent.parent
E2E_LOG = Path(os.environ.get("LOGSTATS_E2E_LOG", REPO / "apache_log.txt"))
E2E_DB = Path(
    os.environ.get("LOGSTATS_E2E_DB", REPO / "geolite2" / "GeoLite2-Country.mmdb")
)
EXPECTED_DB_BUILD = date(2026, 10, 16)

EXPECTED_OS = """OS:
Windows 33.15%
Unknown 24.50%
Linux 14.57%
Mac OS X 14.44%
Ubuntu 6.75%
iOS 4.29%
Android 2.04%
Chrome OS 0.09%
FreeBSD 0.06%
CentOS 0.05%
NetBSD 0.02%
OpenBSD 0.01%
Solaris 0.01%
Windows Mobile 0.01%
Windows Phone 0.01%
"""


def run_cli(*arguments: str | Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "logstats", *map(str, arguments)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def sections(report: str) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    for line in report.splitlines():
        if line.endswith(":"):
            current = parsed.setdefault(line[:-1], [])
        else:
            current.append(line)
    return parsed


def hundredths_sum(rows: list[str]) -> int:
    return sum(int(row.rsplit(" ", 1)[1].rstrip("%").replace(".", "")) for row in rows)


def assert_fails_with_one_line(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 1
    assert result.stdout == ""
    assert len(result.stderr.splitlines()) == 1


@pytest.fixture
def write_log(tmp_path: Path) -> Callable[[str], Path]:
    def write(text: str) -> Path:
        log = tmp_path / "access.log"
        log.write_text(text)
        return log

    return write


def test_report_goes_to_stdout_and_run_summary_to_stderr(
    write_log: Callable[[str], Path],
) -> None:
    result = run_cli(write_log(UK_CHROME_ON_MAC_LINE + GARBAGE_LINE), "--db", TEST_DB)

    assert result.returncode == 0
    assert result.stdout == (
        "Country:\nUnited Kingdom 50.00%\nUnknown 50.00%\n"
        "OS:\nMac OS X 50.00%\nUnknown 50.00%\n"
        "Browser:\nChrome 50.00%\nUnknown 50.00%\n"
    )
    assert result.stderr.splitlines() == [
        "requests: 2",
        "unparsed: 1",
        "unknown: Country 1, OS 1, Browser 1",
        "geolite2 build: 2026-10-14",
        "ua-parser-builtins: 202610",
    ]


def test_missing_database_fails_before_reading_the_log(tmp_path: Path) -> None:
    result = run_cli(tmp_path / "absent.log", "--db", tmp_path / "absent.mmdb")

    assert_fails_with_one_line(result)
    assert "absent.mmdb" in result.stderr


def test_corrupt_database_fails_instead_of_reporting_unknown(
    tmp_path: Path, write_log: Callable[[str], Path]
) -> None:
    corrupt = tmp_path / "corrupt.mmdb"
    corrupt.write_bytes(TEST_DB.read_bytes()[:-200])

    result = run_cli(write_log(CHROME_ON_MAC_LINE), "--db", corrupt)

    assert_fails_with_one_line(result)


def test_database_corrupt_past_its_header_fails_with_one_line(
    tmp_path: Path, write_log: Callable[[str], Path]
) -> None:
    corrupt = tmp_path / "corrupt-tree.mmdb"
    corrupt.write_bytes(b"\xff" * 512 + TEST_DB.read_bytes()[512:])

    result = run_cli(write_log(UK_CHROME_ON_MAC_LINE), "--db", corrupt)

    assert_fails_with_one_line(result)


def test_database_that_is_not_a_country_database_fails_with_one_line(
    tmp_path: Path, write_log: Callable[[str], Path]
) -> None:
    other_type = tmp_path / "city.mmdb"
    other_type.write_bytes(
        TEST_DB.read_bytes().replace(b"GeoLite2-Country", b"GeoLite2-Cxuntry")
    )

    result = run_cli(write_log(CHROME_ON_MAC_LINE), "--db", other_type)

    assert_fails_with_one_line(result)
    assert "GeoLite2-Cxuntry" in result.stderr


def test_missing_log_fails_with_one_line(tmp_path: Path) -> None:
    result = run_cli(tmp_path / "absent.log", "--db", TEST_DB)

    assert_fails_with_one_line(result)
    assert "absent.log" in result.stderr


def test_log_with_no_matching_line_fails_instead_of_reporting_all_unknown(
    write_log: Callable[[str], Path],
) -> None:
    result = run_cli(write_log(GARBAGE_LINE * 3), "--db", TEST_DB)

    assert_fails_with_one_line(result)
    assert "Apache combined" in result.stderr


@pytest.mark.parametrize("text", ["", "\n  \n"], ids=["empty", "blank_lines"])
def test_log_with_no_requests_fails_with_one_line(
    write_log: Callable[[str], Path], text: str
) -> None:
    result = run_cli(write_log(text), "--db", TEST_DB)

    assert_fails_with_one_line(result)
    assert "Apache combined" in result.stderr


def test_missing_arguments_are_a_usage_error() -> None:
    assert run_cli().returncode == 2


def test_stdout_closed_before_the_report_ends_the_run_quietly(
    write_log: Callable[[str], Path],
) -> None:
    log = write_log(UK_CHROME_ON_MAC_LINE)
    read_end, write_end = os.pipe()
    os.close(read_end)

    with os.fdopen(write_end, "w") as pipe_without_reader:
        result = subprocess.run(
            [sys.executable, "-m", "logstats", str(log), "--db", str(TEST_DB)],
            stdout=pipe_without_reader,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=False,
        )

    assert result.returncode == 1
    assert result.stderr == ""


def test_discard_stdout_drops_everything_written_after_it() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from logstats.cli import discard_stdout; discard_stdout(); print('dropped')",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""


def test_real_log_rows_independent_of_the_database_build_match_the_recorded_report() -> (
    None
):
    result = run_cli(E2E_LOG, "--db", E2E_DB)
    report = sections(result.stdout)

    assert result.returncode == 0
    assert result.stderr.splitlines()[:2] == ["requests: 10000", "unparsed: 1"]
    assert list(report) == ["Country", "OS", "Browser"]
    assert all(hundredths_sum(rows) == 10000 for rows in report.values())
    assert "OS:\n" + "\n".join(report["OS"]) + "\n" == EXPECTED_OS
    assert report["Browser"][:4] == [
        "Chrome 28.92%",
        "Firefox 26.07%",
        "Unknown 11.35%",
        "Googlebot 5.09%",
    ]


def test_real_log_country_rows_match_on_the_recorded_database_build() -> None:
    with geoip2.database.Reader(E2E_DB) as reader:
        build = datetime.fromtimestamp(reader.metadata().build_epoch, UTC).date()
    if build != EXPECTED_DB_BUILD:
        pytest.skip(
            f"Country rows were recorded on the {EXPECTED_DB_BUILD} GeoLite2 build, this one is {build}"
        )

    report = sections(run_cli(E2E_LOG, "--db", E2E_DB).stdout)

    assert report["Country"][:3] == [
        "United States 39.10%",
        "France 8.66%",
        "Germany 5.73%",
    ]
    assert "Unknown 0.27%" in report["Country"]

import argparse
import importlib.metadata
import os
import sys
from datetime import UTC, date, datetime
from pathlib import Path

import geoip2.database
import maxminddb

from logstats.dimensions import UNKNOWN, default_dimensions
from logstats.lookups import agent_lookup, country_lookup
from logstats.parse import read_records
from logstats.render import render_text
from logstats.report import Report, aggregate


def arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="logstats",
        description="Statistical report of the percentage of requests per Country, OS and Browser in an Apache web server log file.",
    )
    parser.add_argument(
        "log", type=Path, help="Apache web server log file (combined format)"
    )
    parser.add_argument(
        "--db", type=Path, required=True, help="GeoLite2-Country .mmdb file"
    )
    return parser.parse_args(argv)


def summary(report: Report, db_build: date) -> str:
    unknown = ", ".join(
        f"{name} {counts[UNKNOWN]}" for name, counts in report.counts.items()
    )
    return (
        f"requests: {report.total}\n"
        f"unparsed: {report.unparsed}\n"
        f"unknown: {unknown}\n"
        f"geolite2 build: {db_build}\n"
        f"ua-parser-builtins: {importlib.metadata.version('ua-parser-builtins')}\n"
    )


def fail(message: str) -> int:
    print(f"logstats: {message}", file=sys.stderr)
    return 1


def discard_stdout() -> None:
    os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())


def main(argv: list[str] | None = None) -> int:
    args = arguments(argv)
    try:
        with geoip2.database.Reader(args.db) as reader:
            metadata = reader.metadata()
            if "Country" not in metadata.database_type:
                return fail(
                    f"{args.db} is a {metadata.database_type} database, not GeoLite2-Country"
                )
            dimensions = default_dimensions(country_lookup(reader), agent_lookup())
            with args.log.open(encoding="utf-8", errors="replace") as lines:
                report = aggregate(read_records(lines), dimensions)
    except OSError as error:
        return fail(
            f"cannot read {os.fsdecode(error.filename or args.log)}: {error.strerror}"
        )
    except maxminddb.InvalidDatabaseError as error:
        return fail(f"cannot read GeoLite2 database {args.db}: {error}")
    if report.unparsed == report.total:
        return fail(f"no line in {args.log} is in Apache combined format")
    db_build = datetime.fromtimestamp(metadata.build_epoch, UTC).date()
    try:
        sys.stdout.write(render_text(report))
        sys.stdout.flush()
    except BrokenPipeError:
        discard_stdout()
        return 1
    sys.stderr.write(summary(report, db_build))
    return 0

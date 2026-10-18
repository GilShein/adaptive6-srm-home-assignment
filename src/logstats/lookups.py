import ipaddress
from collections.abc import Callable
from functools import lru_cache

import geoip2.database
import geoip2.errors
import ua_parser

from logstats.dimensions import UNKNOWN, Agent

CACHE_SIZE = 65536


def family_or_unknown(
    part: ua_parser.OS | ua_parser.UserAgent | None,
) -> str:
    if part is None or part.family == "Other":
        return UNKNOWN
    return part.family


def parse_agent(ua: str) -> Agent:
    result = ua_parser.parse(ua)
    return Agent(
        os=family_or_unknown(result.os),
        browser=family_or_unknown(result.user_agent),
    )


def agent_lookup() -> Callable[[str], Agent]:
    return lru_cache(maxsize=CACHE_SIZE)(parse_agent)


def country_lookup(reader: geoip2.database.Reader) -> Callable[[str], str]:
    @lru_cache(maxsize=CACHE_SIZE)
    def country_of(ip: str) -> str:
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return UNKNOWN
        try:
            name = reader.country(ip).country.name
        except geoip2.errors.AddressNotFoundError:
            return UNKNOWN
        return name or UNKNOWN

    return country_of

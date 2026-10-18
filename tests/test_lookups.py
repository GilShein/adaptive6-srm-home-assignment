from collections.abc import Iterator

import geoip2.database
import pytest
from support import CHROME_ON_MAC_AGENT, FIREFOX_ON_UBUNTU_AGENT, TEST_DB

from logstats.dimensions import UNKNOWN
from logstats.lookups import agent_lookup, country_lookup


@pytest.fixture
def reader() -> Iterator[geoip2.database.Reader]:
    with geoip2.database.Reader(TEST_DB) as opened:
        yield opened


def test_country_is_the_english_name_of_the_country_field(
    reader: geoip2.database.Reader,
) -> None:
    country_of = country_lookup(reader)

    assert country_of("81.2.69.160") == "United Kingdom"
    assert country_of("89.160.20.128") == "Sweden"


def test_address_missing_from_the_database_is_unknown(
    reader: geoip2.database.Reader,
) -> None:
    assert country_lookup(reader)("8.8.8.8") == UNKNOWN


def test_text_that_is_not_an_ip_is_unknown(reader: geoip2.database.Reader) -> None:
    assert country_lookup(reader)("not-an-ip") == UNKNOWN


def test_agent_families_come_from_the_ua_rules() -> None:
    agent_of = agent_lookup()
    chrome_on_mac = agent_of(CHROME_ON_MAC_AGENT)
    firefox_on_ubuntu = agent_of(FIREFOX_ON_UBUNTU_AGENT)

    assert (chrome_on_mac.os, chrome_on_mac.browser) == ("Mac OS X", "Chrome")
    assert (firefox_on_ubuntu.os, firefox_on_ubuntu.browser) == ("Ubuntu", "Firefox")


def test_crawler_is_a_browser_family_with_unknown_os() -> None:
    agent = agent_lookup()(
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html"
    )

    assert (agent.os, agent.browser) == (UNKNOWN, "Googlebot")


def test_dash_or_unrecognised_agent_is_unknown_everywhere() -> None:
    agent_of = agent_lookup()
    dash = agent_of("-")
    unrecognised = agent_of(
        "UniversalFeedParser/4.2-pre-314-svn +http://feedparser.org/"
    )

    assert (dash.os, dash.browser) == (UNKNOWN, UNKNOWN)
    assert (unrecognised.os, unrecognised.browser) == (UNKNOWN, UNKNOWN)


def test_rule_that_names_the_os_other_still_reads_unknown() -> None:
    agent = agent_lookup()(
        "Mozilla/5.0 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)"
    )

    assert agent.os == UNKNOWN

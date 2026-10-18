from pathlib import Path

from logstats.dimensions import UNKNOWN, Agent, Dimension, default_dimensions

TEST_DB = Path(__file__).parent / "data" / "GeoLite2-Country-Test.mmdb"

CHROME_ON_MAC_LINE = (
    '83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" '
    '200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" '
    '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"\n'
)
UK_CHROME_ON_MAC_LINE = CHROME_ON_MAC_LINE.replace("83.149.9.216", "81.2.69.160")
DASH_AGENT_LINE = '200.49.190.101 - - [17/May/2015:10:05:36 +0000] "GET /reset.css HTTP/1.1" 200 1015 "-" "-"\n'
FIREFOX_ON_UBUNTU_LINE = (
    '24.236.252.67 - - [17/May/2015:10:05:40 +0000] "GET /favicon.ico HTTP/1.1" 200 3638 "-" '
    '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0"\n'
)
TRUNCATED_AGENT_LINE = (
    '46.118.127.106 - - [20/May/2015:12:05:17 +0000] "GET /scripts/grok-py-test/configlib.py HTTP/1.1" 200 235 "-" '
    '"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html\n'
)
GOOGLEBOT_LINE = (
    '66.249.73.185 - - [17/May/2015:10:05:37 +0000] "GET / HTTP/1.1" 200 37932 "-" '
    '"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"\n'
)
GARBAGE_LINE = "corrupted entry\n"

CHROME_ON_MAC_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
FIREFOX_ON_UBUNTU_AGENT = (
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0"
)

COUNTRIES = {
    "83.149.9.216": "Russia",
    "200.49.190.101": "Guatemala",
    "24.236.252.67": "United States",
}
AGENTS = {
    CHROME_ON_MAC_AGENT: Agent(os="Mac OS X", browser="Chrome"),
    FIREFOX_ON_UBUNTU_AGENT: Agent(os="Ubuntu", browser="Firefox"),
}


def fake_country_of(ip: str) -> str:
    return COUNTRIES.get(ip, UNKNOWN)


def fake_agent_of(ua: str) -> Agent:
    return AGENTS.get(ua, Agent(os=UNKNOWN, browser=UNKNOWN))


def fake_dimensions() -> list[Dimension]:
    return default_dimensions(fake_country_of, fake_agent_of)

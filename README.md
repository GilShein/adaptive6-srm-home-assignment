# Statistical Reporting Module

Reads an Apache web server log file and reports what percentage of requests came from each Country, OS and Browser. The design is in [DESIGN.md](DESIGN.md). The package and its command are called `logstats`.

## Setup

You need [uv](https://docs.astral.sh/uv/). Then run:

```
uv sync
```

## Run

```
uv run logstats apache_log.txt --db geolite2/GeoLite2-Country.mmdb
```

`apache_log.txt` is the assignment's log (10,000 lines), committed at the repo root.

The report is printed to stdout and a short summary to stderr. If the log or the database can't be read, it prints an error and exits with 1. If stdout is closed before the report is written, it stops quietly and exits with 1.

To print only the report, without the summary:

```
uv run logstats apache_log.txt --db geolite2/GeoLite2-Country.mmdb 2>/dev/null
```

## Output

<details>
<summary>Report (stdout)</summary>

```
Country:
United States 39.10%
France 8.66%
Germany 5.73%
Sweden 4.32%
India 4.26%
China 4.16%
United Kingdom 3.11%
Spain 2.22%
Russia 2.03%
Canada 1.97%
Poland 1.49%
Australia 1.39%
Brazil 1.28%
Italy 1.25%
The Netherlands 1.12%
Serbia 1.10%
Austria 1.01%
Ukraine 0.92%
Belgium 0.90%
Japan 0.63%
Czechia 0.62%
Finland 0.61%
Vietnam 0.61%
Greece 0.57%
Israel 0.55%
Hong Kong 0.54%
Türkiye 0.43%
New Zealand 0.42%
Romania 0.42%
Denmark 0.41%
Taiwan 0.38%
Indonesia 0.35%
El Salvador 0.34%
Trinidad and Tobago 0.34%
Slovenia 0.33%
Switzerland 0.32%
Hungary 0.31%
Norway 0.30%
Estonia 0.27%
Lebanon 0.27%
Mexico 0.27%
Slovakia 0.27%
Unknown 0.27%
Argentina 0.26%
Singapore 0.24%
Ireland 0.23%
Latvia 0.23%
Thailand 0.23%
Venezuela 0.19%
Malaysia 0.17%
South Korea 0.17%
Chile 0.16%
Croatia 0.16%
Kazakhstan 0.16%
Bulgaria 0.14%
Philippines 0.14%
Portugal 0.13%
Lithuania 0.12%
Moldova 0.10%
South Africa 0.09%
Algeria 0.08%
Bosnia and Herzegovina 0.08%
Iran 0.08%
Mozambique 0.07%
Peru 0.07%
Belarus 0.06%
Egypt 0.06%
Montenegro 0.06%
Morocco 0.06%
Qatar 0.06%
Rwanda 0.06%
Guatemala 0.05%
United Arab Emirates 0.05%
Colombia 0.04%
Iraq 0.04%
Saudi Arabia 0.04%
Bangladesh 0.02%
Cambodia 0.02%
Honduras 0.02%
Kenya 0.02%
Luxembourg 0.02%
Myanmar 0.02%
Sudan 0.02%
Syria 0.02%
Azerbaijan 0.01%
Belize 0.01%
Cook Islands 0.01%
Georgia 0.01%
Ghana 0.01%
Kuwait 0.01%
Libya 0.01%
North Macedonia 0.01%
Oman 0.01%
Pakistan 0.01%
Tanzania 0.01%
OS:
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
Browser:
Chrome 28.92%
Firefox 26.07%
Unknown 11.35%
Googlebot 5.09%
IE 4.86%
Safari 2.62%
Tiny Tiny RSS 1.98%
Chromium 1.76%
archive.org_bot 1.66%
Yahoo! Slurp 1.06%
Mobile Safari 1.03%
Opera 0.98%
msnbot 0.96%
Iceweasel 0.93%
Chrome Frame 0.91%
Baiduspider 0.83%
Chrome Mobile 0.78%
Android 0.67%
YandexBot 0.64%
bingbot 0.58%
Feedbin 0.50%
Exabot 0.39%
MJ12bot 0.39%
AhrefsBot 0.34%
Twitterbot 0.28%
Firefox Mobile 0.26%
Chrome Mobile iOS 0.22%
msnbot-media 0.22%
Mail.RU_Bot 0.21%
YandexImages 0.21%
Googlebot-Mobile 0.20%
Midori 0.19%
Sogou web spider 0.18%
Amazon Silk 0.17%
favicon 0.17%
Google 0.15%
FacebookBot 0.14%
Googlebot-Image 0.13%
Opera Mini 0.13%
Mobile Safari UI/WKWebView 0.11%
SeaMonkey 0.10%
robot 0.10%
Liferea 0.09%
VoilaBot 0.09%
BingPreview 0.08%
AppEngine-Google 0.07%
magpie-crawler 0.07%
psbot 0.07%
Conkeror 0.06%
Openwave 0.06%
Wget 0.06%
PhantomJS 0.05%
archiver 0.05%
Chrome Mobile WebView 0.04%
MobileSafari 0.04%
Python-urllib 0.04%
fetch libfetch 0.04%
360Spider 0.03%
Maxthon 0.03%
Newsify 0.03%
Reeder 0.03%
Xenu Link Sleuth 0.03%
ia_archiver 0.03%
AOL 0.02%
BeetleBot 0.02%
Daumoa 0.02%
EasouSpider 0.02%
LumiBot 0.02%
MojeekBot 0.02%
Nutch 0.02%
Rekonq 0.02%
com/bot 0.02%
Apple Mail 0.01%
Baidu Explorer 0.01%
Baiduspider-image 0.01%
Bon Echo 0.01%
ELinks 0.01%
Epiphany 0.01%
Genieo 0.01%
GmailImageProxy 0.01%
IE Mobile 0.01%
Instagram 0.01%
Iron 0.01%
Konqueror 0.01%
Links 0.01%
Lynx 0.01%
Pale Moon 0.01%
Python Requests 0.01%
SEMC-Browser 0.01%
SimplePie 0.01%
Sogou Explorer 0.01%
Thunderbird 0.01%
UC Browser 0.01%
YandexDirect 0.01%
YisouSpider 0.01%
ZDM 0.01%
curl 0.01%
libwww-perl 0.01%
```

</details>
<br>

Summary (stderr) for `apache_log.txt`:

```
requests: 10000
unparsed: 1
unknown: Country 27, OS 2450, Browser 1135
geolite2 build: 2026-10-16
ua-parser-builtins: 202610
```

## Tests

```
uv run pytest
uv run pytest --cov
uv run ruff check .
```

The lookups are passed in (dependency injection), so most tests use fake lookups instead of the real database. The end-to-end tests run on `apache_log.txt` and the database in `geolite2/`. To run them on other files, set `LOGSTATS_E2E_LOG` and `LOGSTATS_E2E_DB`.

`--cov` adds a coverage report. It includes the CLI tests, which run `logstats` in a separate process.

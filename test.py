import pywikibot
from datetime import datetime, timedelta, timezone

site = pywikibot.Site("en", "wikipedia")
user = pywikibot.User(site, "Ow0castBot")

target = "Debian"

last = None
for page, revid, timestamp, comment in user.contributions():
    if page.title() == target:
        last = timestamp
        break

if last:
    now = datetime.now(timezone.utc)
    diff = now - last
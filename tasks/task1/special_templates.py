import mwparserfromhell
import re

def _WANTS_PLAIN_TITLE_INSTEAD_OF_WIKILINK(content):
    return re.sub(r"(https?(:\/\/)?)\w+\.wikipedia.org/wiki/", "", content)

TREAT_SPECIAL = {
    "disputed inline": {
        "talkpage": _WANTS_PLAIN_TITLE_INSTEAD_OF_WIKILINK,
        "talk": _WANTS_PLAIN_TITLE_INSTEAD_OF_WIKILINK,
        "discuss": _WANTS_PLAIN_TITLE_INSTEAD_OF_WIKILINK,
        "discussion": _WANTS_PLAIN_TITLE_INSTEAD_OF_WIKILINK
    }
}

SKIP = [
    "url",
    "reflist",
    "not a typo",
    "official website",
    "basketball roster footer",
    "url",
    "coloredlink",
    "colored link",
    "free-content attribution",
    "creative commons text attribution notice",
    "cc-notice"
]

CITATIONS = [
    "citation",
    "cite",
    "cite book",
    "cite journal",
    "cite web",
    "cite comic",
    "cite conference",
    "cite court",
    "cite dictionary",
    "cite encyclopedia",
    "cite episode",
    "cite mailing list",
    "cite map",
    "cite news",
    "cite newsgroup",
    "cite patent",
    "cite press release",
    "cite av media",
    "cite video game",
    "cite q"
    "cite arxiv",
    "cite av media",
    "cite av media notes",
    "cite biotxiv",
    "cite book",
    "cite citeseerx",
    "cite conference",
    "cite document",
    "cite encyclopedia",
    "cite episode",
    "cite interview",
    "cite journal",
    "cite magazine",
    "cite mailing list",
    "cite map",
    "cite medrxiv",
    "cite news",
    "cite newsgroup",
    "cite podcast",
    "cite press release",
    "cite report",
    "cite serial",
    "cite sign",
    "cite speech",
    "cite ssrn",
    "cite tech report",
    "cite thesis",
    "cite web"
]
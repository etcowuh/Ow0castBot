from tasks.BaseTask import BaseTask

from tasks.task1.special_templates import SKIP, TREAT_SPECIAL, CITATIONS

import mwparserfromhell
from pywikibot import pagegenerators
import pywikibot
import re
from urllib.parse import unquote, urlparse
import difflib
from colorama import Fore, Style, init
from datetime import datetime, timezone, timedelta
class Task1(BaseTask):
    def __init__(self):
        super().__init__(1, "Replace plain links to wikipedia with wikilinks")
        self.template_cache = []
        self.links_in_refs = []
        self.links_in_wikilinks = []

    def _is_too_soon(self, target):
        last = None
        for page, revid, timestamp, comment in self.user.contributions():
            if page.title() == target:
                last = timestamp
            break
        if last:
            now = datetime.now(timezone.utc)
            diff = now - last

            if diff > timedelta(hours=24):
                return False
            else:
                return True
        else:
            return False

    def can_edit(self, page):
        user = "Ow0castBot"
        text = mwparserfromhell.parse(page.text)
        for tl in text.filter_templates():
            if tl.name.matches(['bots', 'nobots']):
                break
        else:
            return True
        for param in tl.params:
            bots = [x.lower().strip() for x in param.value.split(",")]
            if param.name == 'allow':
                if ''.join(bots) == 'none': return False
                for bot in bots:
                    if bot in (user, 'all'):
                        return True
            elif param.name == 'deny':
                if ''.join(bots) == 'none': return True
                for bot in bots:
                    if bot in (user, 'all'):
                        return False
        if (tl.name.matches('nobots') and len(tl.params) == 0):
            return False
        return True

    def _preprocess(self, wikicode):
        super()._preprocess(wikicode)
        self.template_cache = []
        self.links_in_refs = []
        self.links_in_wikilinks = []

        templates = wikicode.filter_templates(False)
        for template in templates:
            if any(template.name.lower().strip() == t for t in SKIP) or any(template.name.lower().strip() == c for c in CITATIONS):
                self.template_cache.append(str(template))
                wikicode.replace(template, f"__fXfSkJNltGndYxvKtpPvrOOCupTjxNcy_{str(len(self.template_cache) - 1)}_If_you_see_this_in_an_article_tell_[[User:Ow0cast]]")
            if any(template.name.lower().strip() == t for t in TREAT_SPECIAL):
                for param in template.params:
                    name = str(param.name).strip()
                    value = str(param.value)
                    handler = TREAT_SPECIAL.get(str(template.name).lower().strip(), {}).get(name.lower())
                    if handler:
                        param.value = handler(value)
        for tag in wikicode.filter_tags():
            if tag.tag and tag.tag.lower() == "ref":
                self.links_in_refs.extend(mwparserfromhell.parse(tag).filter_external_links())
        for wl in wikicode.filter_wikilinks():
            self.links_in_wikilinks.extend(mwparserfromhell.parse(wl).filter_external_links())
        return wikicode

    def _process(self, wikicode):
        links = wikicode.filter_external_links()
        for link in links:
            if any(link is ref_link for ref_link in self.links_in_refs):
                continue
            if re.match(r"(https?(:\/\/)?)\w+\.wikipedia.org/wiki/", str(link.url)):
                # dude what the fuck is this code
                url_str = str(link.url)
                rest = ""
                title = str(link.title) if link.title else ""
                if "|" in url_str:
                    pipe_idx = url_str.index("|")
                    pipe_tail = url_str[pipe_idx + 1:]
                    url_str = url_str[:pipe_idx]
                    if title:
                        title = pipe_tail + " " + title
                    else:
                        rest = "|" + pipe_tail

                clean = urlparse(unquote(url_str))._replace(query=None).geturl()
                page = clean.split("/wiki/")[1].split("#:~:")[0]
                lang = clean.split("://")[1].split(".")[0]

                is_in_wikilink = any(link is wl_link for wl_link in self.links_in_wikilinks)

                new = ""
                if page.lower().startswith("file"):
                    self._log_state(f"Skipping {link.url} because it is a File link")
                    continue
                if is_in_wikilink:
                    if lang == self.site.lang:
                        new = f"{page}{rest}"
                    else:
                        new = f"{lang}:{page}{rest}"
                else:
                    if lang == self.site.lang:
                        if title:
                            new = f"[[{page}|{title}]]{rest}"
                        else:
                            new = f"[[{page}]]{rest}"
                    else:
                        if title:
                            new = f"[[{lang}:{page}|{title}]]{rest}"
                        else:
                            new = f"[[{lang}:{page}]]{rest}"
                    ensureProperNamednessArray = mwparserfromhell.parse(new).filter_wikilinks(False)
                    if len(ensureProperNamednessArray) != 1:
                        new = str(ensureProperNamednessArray[-1]) + rest
                            
                    try:
                        idx = wikicode.index(link)
                        if idx > 0 and idx < len(wikicode.nodes) - 1:
                            prev_node = wikicode.nodes[idx - 1]
                            next_node = wikicode.nodes[idx + 1]
                            if isinstance(prev_node, mwparserfromhell.nodes.text.Text) and isinstance(next_node, mwparserfromhell.nodes.text.Text):
                                if prev_node.value.endswith("[") and next_node.value.startswith("]"):
                                    prev_node.value = prev_node.value[:-1]
                                    next_node.value = next_node.value[1:]
                    except ValueError:
                        pass
                        
                wikicode.replace(link, str(new).replace("_", " "))
        return wikicode

    def _postprocess(self, wikicode):
        for i, template in enumerate(self.template_cache):
            wikicode.replace(f"__fXfSkJNltGndYxvKtpPvrOOCupTjxNcy_{str(i)}_If_you_see_this_in_an_article_tell_[[User:Ow0cast]]", template)
        return wikicode

    def run(self, site: pywikibot.Site):
        self.site = site
        self.user = pywikibot.User(site, "Ow0castBot")
        generator = pywikibot.pagegenerators.TextIOPageGenerator("pages_task1.txt")
        for currentPage in generator:
            self.state = 0
            self._log_state(f"On [[{currentPage.title()}]]:")
            if not self.can_edit(currentPage.text):
                self._log_state("Not allowed to edit this page")
                self._log_state("")
                continue
            if self._is_too_soon(currentPage):
                self._log_state("Too soon to edit this page again")
                self._log_state("")
                continue
            wikicode = mwparserfromhell.parse(currentPage.text)
            wikicode = self._preprocess(wikicode)
            wikicode = self._process(wikicode)
            wikicode = self._postprocess(wikicode)
            self.state = 4
            if currentPage.text == wikicode:
                self._log_state("Nothing to do.")
                self._log_state("")
            else:
                diff = difflib.ndiff(
                    currentPage.text.split("\n"),
                    str(wikicode).split("\n")
                )
                for line in diff:
                    if line.startswith('+ '):
                        print(Fore.GREEN + line + Fore.RESET)
                    elif line.startswith('- '):
                        print(Fore.RED + line + Fore.RESET)
                    elif line.startswith('? '):
                        print(Fore.BLUE + line + Fore.RESET)
                    else:
                        print(line)
                if input("OK? (y/n) ") == "y":
                    currentPage.text = wikicode
                    currentPage.save(f"supervised while on trial | {self.description} | [[Wikipedia:Bots/Requests_for_approval/Ow0castBot|BRFA]]")
                    self._log_state("")
                else:
                    self._log_state("Not saving.")
                    self._log_state("")
        # self.logger.info("Task 1 completed")

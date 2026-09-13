import os
import sys
import pywikibot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks.task import run_tasks

if __name__ == "__main__":
    run_tasks(pywikibot.Site("en", "wikipedia"))

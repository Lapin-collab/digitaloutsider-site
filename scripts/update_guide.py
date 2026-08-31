"""Refresh gamecopilot/guide.html from the app repo's docs export.

Run from the site repo root after rebuilding the docs HTML in the app repo
(C:\\GameCopilot: `.venv\\Scripts\\python.exe scripts\\build_docs_html.py`):

    python scripts\\update_guide.py

The site guide = site-specific head (SEO metas + the light/dark variable
stylesheet + favicon) + the docs export's BODY + the goatcounter tag.
This script keeps the existing head/tail of gamecopilot/guide.html and
transplants only the body from C:\\GameCopilot\\docs\\USER_GUIDE.en.html —
so styling/SEO edits made here survive doc updates, and doc updates never
have to be re-applied by hand (committed on purpose, v0.6.1: the previous
refresh was an ad-hoc never-recorded procedure).
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent
GUIDE = SITE / "gamecopilot" / "guide.html"
DOCS_EXPORT = pathlib.Path(r"C:\GameCopilot\docs\USER_GUIDE.en.html")


def body_of(html: str) -> str:
    m = re.search(r"<body>(.*)</body>", html, re.S)
    if not m:
        raise SystemExit("no <body>…</body> found")
    return m.group(1)


site_html = GUIDE.read_text(encoding="utf-8")
docs_html = DOCS_EXPORT.read_text(encoding="utf-8")

head, old_body_and_tail = site_html.split("<body>", 1)
_old_body, tail = old_body_and_tail.rsplit("</body>", 1)
# keep the trailing analytics <script> that lives INSIDE the old body
m = re.search(r"(<script data-goatcounter.*?</script>)", _old_body, re.S)
analytics = m.group(1) if m else ""

new_html = (head + "<body>" + body_of(docs_html) + analytics
            + "</body>" + tail)
GUIDE.write_text(new_html, encoding="utf-8")
print(f"guide.html refreshed: {len(new_html)} bytes "
      f"(body from {DOCS_EXPORT.name})")

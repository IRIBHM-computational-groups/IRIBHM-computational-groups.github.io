"""
Turn the raw HTML that mammoth produces from SAFE.docx into a structured,
readable web page.

The Word document has no heading styles at all: every line is a plain
paragraph, so mammoth returns one long flat list of <p> elements. This module
recovers the structure from a handful of simple, explainable rules, and returns
both the restructured HTML and a table of contents.

Rules used to detect headings
-----------------------------
1. The first two paragraphs are the document title and subtitle.
2. A paragraph that is entirely bold + italic ("SAFE Guidelines: SAFE Teams")
   starts a new top-level section  -> <h2>
3. A paragraph that is entirely italic and starts with "We commit"
   ("We commit to publicly document:") becomes a commitment banner.
4. Any other fully italic paragraph ("What are the core working hours?")
   -> <h3>. A paragraph that merely starts in italics and asks a question is
   treated the same way, because the Word file is inconsistent there.
5. A short plain paragraph with no sentence-ending punctuation
   ("Diversity statement", "Shared lab calendar")  -> <h3>
   Ending in ":" keeps it a normal lead-in paragraph, which is what the
   document intends ("Mandatory viewing for new members:").
6. A numbered list with a single item is a numbered heading in disguise
   -> <h3>, or <h4> when it ends with ":" (e.g. "Lab meetings:")
7. Empty paragraphs are dropped, and tables get a header row plus a wrapper
   that allows horizontal scrolling on phones.

If the Word document changes, these rules still apply; only add an entry to
FORCE_HEADING / NEVER_HEADING below if a specific line is misclassified.
"""

import re
import unicodedata

# Name given to the first section, which has no title in the Word document.
FIRST_SECTION_TITLE = "Lab policies"

# Escape hatches for lines the rules above would get wrong.
FORCE_HEADING = set()       # exact text -> always treat as a heading
NEVER_HEADING = set()       # exact text -> never treat as a heading

MAX_HEADING_CHARS = 75


# --------------------------------------------------------------------------- #
# Splitting the flat HTML into top-level blocks
# --------------------------------------------------------------------------- #

BLOCK_RE = re.compile(r"<(p|ul|ol|table|h[1-6])\b", re.I)


def _split_blocks(html):
    """Yield the top-level blocks (<p>, <ul>, <ol>, <table>, ...) in order."""
    blocks = []
    pos = 0
    while True:
        m = BLOCK_RE.search(html, pos)
        if not m:
            break
        tag = m.group(1).lower()
        start = m.start()
        # Walk forward counting opening/closing tags of the same name so that
        # nested lists are kept inside their parent block.
        depth = 0
        scan = start
        tag_re = re.compile(r"<(/?)%s\b[^>]*?(/?)>" % tag, re.I)
        while True:
            t = tag_re.search(html, scan)
            if not t:
                scan = len(html)
                break
            closing, self_closing = t.group(1), t.group(2)
            if self_closing:
                pass
            elif closing:
                depth -= 1
            else:
                depth += 1
            scan = t.end()
            if depth == 0:
                break
        blocks.append(html[start:scan])
        pos = scan
    return blocks


def _text_of(block):
    """Plain text of a block, tags and entities removed."""
    text = re.sub(r"<[^>]+>", "", block)
    text = (text.replace("&amp;", "&").replace("&lt;", "<")
                .replace("&gt;", ">").replace("&nbsp;", " ")
                .replace("&#39;", "'").replace("&quot;", '"'))
    return re.sub(r"\s+", " ", text).strip()


def _inner(block):
    """Contents of a block, without its outer tag."""
    return re.sub(r"^<[^>]+>|</[^>]+>$", "", block.strip())


def _strip_wrapper(inner, *tags):
    """Remove a formatting tag that wraps the whole content."""
    for tag in tags:
        m = re.fullmatch(r"\s*<%s>(.*)</%s>\s*" % (tag, tag), inner,
                         re.S | re.I)
        if m:
            inner = m.group(1)
    return inner


def _wrapped_in(inner, *tags):
    """True when the whole paragraph is wrapped in the given tag(s)."""
    stripped = inner.strip()
    for tag in tags:
        m = re.fullmatch(r"<%s>(.*)</%s>" % (tag, tag), stripped, re.S | re.I)
        if not m:
            return False
        stripped = m.group(1).strip()
    return True


def _slug(text, used):
    """A readable, unique id for anchor links."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "section"
    candidate, n = slug, 2
    while candidate in used:
        candidate, n = "%s-%d" % (slug, n), n + 1
    used.add(candidate)
    return candidate


# --------------------------------------------------------------------------- #
# Classifying a block
# --------------------------------------------------------------------------- #

def _is_plain_heading(text, block):
    """Rule 5: a short plain line with no sentence-ending punctuation."""
    if not block.lower().startswith("<p"):
        return False
    if len(text) > MAX_HEADING_CHARS or len(text) < 3:
        return False
    if text[-1] in ".:?!;,":
        return False
    if re.search(r"<(a|img|table)\b", block, re.I):
        return False
    return True


def _classify(block):
    """Return (kind, text) where kind is section/commit/h3/h4/body."""
    text = _text_of(block)
    if not text and not re.search(r"<(img|table)\b", block, re.I):
        return "drop", ""
    if text in NEVER_HEADING:
        return "body", text
    if text in FORCE_HEADING:
        return "h3", text

    if block.lower().startswith("<p"):
        inner = _inner(block)
        # Rule 2: bold + italic -> new top-level section
        if _wrapped_in(inner, "strong", "em") or _wrapped_in(inner, "em", "strong"):
            return "section", text
        # Rules 3 and 4: fully italic paragraphs
        if _wrapped_in(inner, "em"):
            if text.lower().startswith("we commit"):
                return "commit", text
            return "h3", _tidy_heading(text)
        # Rule 4b: some question headings are only partly italic in Word
        if (inner.lstrip().lower().startswith("<em>") and text.endswith("?")
                and len(text) <= 160 and "<a " not in block.lower()):
            return "h3", _tidy_heading(text)
        if _is_plain_heading(text, block):
            return "h3", _tidy_heading(text)

    # Rule 6: a one-item numbered list is a numbered heading
    if block.lower().startswith("<ol") and block.lower().count("<li") == 1:
        if len(text) <= 110:
            return "h4" if text.endswith(":") else "h3", text.rstrip(":")

    return "body", text


# --------------------------------------------------------------------------- #
# Tidying individual blocks
# --------------------------------------------------------------------------- #

def _tidy_heading(text):
    """Tidy Word's French-style spacing before punctuation in headings."""
    return re.sub(r"\s+([?:;!])", r"\1", text).strip()


DASH_ONLY = re.compile(r"^[\u2014\u2013\-\s]+$")


def _tidy_table(block):
    """Add a header row, mark empty cells, and allow horizontal scrolling."""
    rows = re.findall(r"<tr>.*?</tr>", block, re.S | re.I)
    if not rows:
        return block

    def cell_fix(row, cell_tag):
        def repl(m):
            content = m.group(1)
            if DASH_ONLY.match(_text_of(content)):
                return "<%s class=\"na\"><span aria-hidden=\"true\">–</span>"\
                       "<span class=\"visually-hidden\">not applicable</span>"\
                       "</%s>" % (cell_tag, cell_tag)
            return "<%s>%s</%s>" % (cell_tag, content, cell_tag)
        return re.sub(r"<td>(.*?)</td>", repl, row, flags=re.S | re.I)

    def build_row(row):
        cells = re.findall(r"<td>(.*?)</td>", row, re.S | re.I)
        # A row whose value cells are all dashes is a category header
        is_group = len(cells) > 1 and all(DASH_ONLY.match(_text_of(c))
                                          for c in cells[1:])
        fixed = cell_fix(row, "td")
        if is_group:
            fixed = fixed.replace("<tr>", '<tr class="group">', 1)
        return fixed

    head = cell_fix(rows[0], "th")
    body = "".join(build_row(r) for r in rows[1:])
    return ('<div class="table-scroll"><table class="roles-table">'
            "<thead>%s</thead><tbody>%s</tbody></table></div>" % (head, body))


def _tidy_paragraph(block):
    """Drop stray line breaks and non-breaking spaces left by Word."""
    block = re.sub(r"(<br\s*/?>)+\s*</p>", "</p>", block, flags=re.I)
    return block


# --------------------------------------------------------------------------- #
# Main entry point
# --------------------------------------------------------------------------- #

def structure_guidelines(html):
    """
    Restructure mammoth's output.

    Returns (html, toc) where toc is a list of dicts:
        {"id": ..., "title": ..., "children": [{"id": ..., "title": ...}, ...]}
    """
    blocks = _split_blocks(html)
    if not blocks:
        return html, []

    classified = [(_classify(b) + (b,)) for b in blocks]
    classified = [c for c in classified if c[0] != "drop"]

    # The first two lines are the document title and subtitle.
    title = subtitle = ""
    while classified and not title:
        kind, text, block = classified.pop(0)
        title = text
    if classified:
        kind, text, block = classified[0]
        if kind in ("h3", "section", "body") and len(text) <= MAX_HEADING_CHARS:
            subtitle = text
            classified.pop(0)

    used_ids = set()
    toc = []
    out = []
    open_section = False

    def close_section():
        nonlocal open_section
        if open_section:
            out.append("</section>")
            open_section = False

    def open_new_section(text):
        nonlocal open_section
        close_section()
        sid = _slug(text, used_ids)
        toc.append({"id": sid, "title": text, "children": []})
        out.append('<section class="guideline-section" id="%s">' % sid)
        out.append('<h2><a class="anchor" href="#%s">%s</a></h2>' % (sid, text))
        open_section = True

    # Everything before the first explicit "SAFE Guidelines:" line belongs to
    # an unnamed opening section.
    if not any(k == "section" for k, _, _ in classified[:1]):
        open_new_section(FIRST_SECTION_TITLE)

    for kind, text, block in classified:
        if kind == "section":
            open_new_section(text)
        elif kind == "commit":
            label = text.rstrip(":")
            out.append('<p class="commitment">%s</p>' % label)
        elif kind in ("h3", "h4"):
            hid = _slug(text, used_ids)
            level = 3 if kind == "h3" else 4
            if toc and level == 3:
                toc[-1]["children"].append({"id": hid, "title": text})
            out.append('<h%d id="%s"><a class="anchor" href="#%s">%s</a></h%d>'
                       % (level, hid, hid, text, level))
        elif block.lower().startswith("<table"):
            out.append(_tidy_table(block))
        else:
            out.append(_tidy_paragraph(block))

    close_section()

    header = ""
    if title:
        header = '<h1 class="doc-title">%s</h1>' % title
        if subtitle:
            header += '<p class="doc-subtitle">%s</p>' % subtitle

    return header + "\n".join(out), toc

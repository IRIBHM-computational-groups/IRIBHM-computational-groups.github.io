import requests
import pandas as pd

# ---------------------------------------------------------------------------
# OpenAlex asks API users to identify themselves; in exchange we get the fast,
# reliable "polite pool". Put a real address here.
# ---------------------------------------------------------------------------
MAILTO = "maxime.tarabichi@ulb.be"

# Asking for gzip only also avoids the brotli decoding bug in some installs.
HEADERS = {
    "User-Agent": f"IRIBHM-computational-groups website (mailto:{MAILTO})",
    "Accept-Encoding": "gzip, deflate",
}

API = "https://api.openalex.org"


def _get(url, params):
    params = dict(params, mailto=MAILTO)
    r = requests.get(url, params=params, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()


def find_author_profiles(author_name, n=5):
    """Print the candidate OpenAlex profiles for a name.

    OpenAlex often splits one researcher over several profiles, and the first
    search hit is not always the right one. Run this once per lab member, then
    hard-code the IDs you recognise in AUTHORS below.
    """
    data = _get(f"{API}/authors", {"search": author_name, "per_page": n})
    for a in data.get("results", []):
        inst = (a.get("last_known_institutions") or [{}])[0].get("display_name", "?")
        print(f"{a['id'].split('/')[-1]:<14} {a['display_name']:<28} "
              f"works={a.get('works_count', 0):<5} orcid={a.get('orcid')} inst={inst}")


def _resolve_author_ids(author):
    """Accept an OpenAlex ID, an ORCID, a name, or a list of any of these."""
    if isinstance(author, (list, tuple, set)):
        ids = []
        for item in author:
            ids += _resolve_author_ids(item)
        return ids

    author = str(author).strip()

    # Plain OpenAlex author ID, e.g. "A5045412483" or the full URL
    if author.upper().startswith("A") and author[1:].isdigit():
        return [author.upper()]
    if "openalex.org/A" in author:
        return [author.rstrip("/").split("/")[-1].upper()]

    # ORCID: the most reliable identifier
    if author.replace("-", "").replace("X", "").isdigit() and author.count("-") == 3:
        data = _get(f"{API}/authors", {"filter": f"orcid:{author}"})
        return [a["id"].split("/")[-1] for a in data.get("results", [])]

    # Fall back to a name search (first hit only, as before)
    data = _get(f"{API}/authors", {"search": author, "per_page": 1})
    if not data.get("results"):
        print(f"  !! no OpenAlex profile found for '{author}'")
        return []
    hit = data["results"][0]
    print(f"  found by name: {hit['display_name']} ({hit['id']}) "
          f"- consider pinning this ID in AUTHORS")
    return [hit["id"].split("/")[-1]]


def get_author_works(author, display_name=None, max_results=None):
    """Return a DataFrame of all works for one person.

    `author` may be a name, an ORCID, an OpenAlex ID, or a list of OpenAlex IDs
    when OpenAlex has split the person over several profiles.
    `display_name` is the name shown on the website (defaults to `author`).
    """
    name = display_name or (author if isinstance(author, str) else str(author))
    author_ids = _resolve_author_ids(author)
    if not author_ids:
        return pd.DataFrame()

    print(f"Fetching works for {name}: {', '.join(author_ids)}")

    works, cursor, seen_pages = [], "*", 0
    while cursor:
        data = _get(f"{API}/works", {
            # "|" means OR, so several profiles are merged in one query
            "filter": f"authorships.author.id:{'|'.join(author_ids)},type:!paratext",
            "per_page": 200,
            "sort": "publication_date:desc",
            "cursor": cursor,
        })
        works += data.get("results", [])
        cursor = data.get("meta", {}).get("next_cursor")
        seen_pages += 1
        if max_results and len(works) >= max_results:
            works = works[:max_results]
            break
        if seen_pages > 25:  # safety valve
            break

    rows = []
    for work in works:
        primary_location = work.get("primary_location") or {}
        source = primary_location.get("source") or {}
        journal = source.get("display_name") or "N/A"
        work_type = work.get("type", "")
        # OpenAlex flags preprints both ways depending on the record
        is_preprint = work_type == "preprint" or (source.get("type") == "repository")

        rows.append({
            "title": work.get("title") or "N/A",
            "year": work.get("publication_year", "N/A"),
            "journal": journal,
            "doi": work.get("doi") or "N/A",
            "cited_by_count": work.get("cited_by_count", 0),
            "type": work_type,
            "is_preprint": is_preprint,
        })

    df = pd.DataFrame(rows)
    if df.empty:
        print(f"  no works found for {name}")
        return pd.DataFrame()

    # Keep anything with a DOI and a source. Note: no citation-count filter,
    # so brand-new papers and preprints are kept.
    df = df[(df["doi"] != "N/A") & (df["journal"] != "N/A")].copy()

    # Drop a preprint when the same title also exists as a published paper
    df["_key"] = df["title"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
    df = df.sort_values("is_preprint").drop_duplicates(subset="_key", keep="first")
    df = df.drop(columns="_key")

    df["person"] = name
    print(f"  {len(df)} works kept")
    return df

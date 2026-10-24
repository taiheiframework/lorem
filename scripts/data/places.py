"""Cities and regions from Wikidata (CC0): the largest cities of a country by population, with
their names in the language and, where the address format names one, their first-level region.
Weights are populations in thousands."""

import romanize
from common import sparql

# The class of a country's first-level subdivisions, for the formats that name a region.
REGION_CLASS = {"US": ["Q35657"], "BR": ["Q485258"], "IN": ["Q12443800", "Q467745"]}

# Places that Wikidata also gives another country, which a country's sample addresses leave out
# (Serbia: the cities of Kosovo).
OTHER_COUNTRY = {"RS": "Q1246"}

# Countries whose cities Wikidata records as dissolved after a reform of local government
# (Vietnam abolished its provincial cities in 2025): their names are still what addresses and
# people use, so a dissolved item counts.
DISSOLVED_OK = {"VN"}

# Cities whose Wikidata class the settlement filter misses (Los Angeles is only a "charter city"),
# taken in with their population like the others.
EXTRA = {"US": ["Q65"]}


def _largest(country, qid, threshold):
    dissolved = "" if country in DISSOLVED_OK else "FILTER NOT EXISTS { ?item wdt:P576 ?end }"
    # The population filter first, then the class: the other way round times out.
    return sparql(f"cities-{country}-{threshold}", f"""
        SELECT ?item (MAX(?p) AS ?pop) WHERE {{
          {{ SELECT ?item ?p WHERE {{ ?item wdt:P17 wd:{qid}; wdt:P1082 ?p . FILTER(?p > {threshold}) }} }}
          # A settlement by at least one class that is not an urban or metropolitan area (of
          # which Wikidata holds many with populations larger than any city's), nor a
          # neighbourhood, quarter or district of a city.
          FILTER EXISTS {{ ?item wdt:P31 ?c . ?c wdt:P279* wd:Q486972 .
                           FILTER NOT EXISTS {{ ?c wdt:P279* wd:Q702492 }}
                           FILTER NOT EXISTS {{ ?c wdt:P279* wd:Q1907114 }}
                           FILTER NOT EXISTS {{ ?c wdt:P279* wd:Q123705 }}
                           FILTER NOT EXISTS {{ ?c wdt:P279* wd:Q2983893 }}
                           FILTER NOT EXISTS {{ ?c wdt:P279* wd:Q4286337 }} }}
          {dissolved}
        }} GROUP BY ?item ORDER BY DESC(?pop) LIMIT 400""")


def cities(country, qid, lang, ok, limit=100):
    """[{name, weight, region?}], the `limit` largest cities whose label in `lang` passes `ok`."""
    rows = []
    for threshold in (100000, 20000, 5000):
        rows = _largest(country, qid, threshold)
        if len(rows) >= limit * 1.2:
            break
    pops = {r["item"]: int(float(r["pop"])) for r in rows}
    if country in OTHER_COUNTRY:
        values = " ".join("wd:" + i.rsplit("/", 1)[1] for i in pops)
        shared = sparql(f"cities-shared-{country}", f"""
            SELECT ?item WHERE {{ VALUES ?item {{ {values} }} ?item wdt:P17 wd:{OTHER_COUNTRY[country]} }}""")
        for r in shared:
            pops.pop(r["item"], None)
    if country in EXTRA:
        extra = sparql(f"cities-extra-{country}", """SELECT ?item (MAX(?p) AS ?pop) WHERE {
            VALUES ?item { %s } ?item wdt:P1082 ?p } GROUP BY ?item""" % " ".join("wd:" + q for q in EXTRA[country]))
        pops.update({r["item"]: int(float(r["pop"])) for r in extra})
    values = " ".join("wd:" + i.rsplit("/", 1)[1] for i in pops)
    region_class = REGION_CLASS.get(country)
    region = ""
    if region_class:
        classes = " ".join("wd:" + c for c in region_class)
        region = f"""OPTIONAL {{ VALUES ?rc {{ {classes} }} ?item wdt:P131* ?r . ?r wdt:P31 ?rc; rdfs:label ?region .
                                FILTER(LANG(?region) = "{lang}") }}"""
    labels = sparql(f"city-labels-{country}-{lang}", f"""
        SELECT ?item ?label {"?region" if region_class else ""} WHERE {{
          VALUES ?item {{ {values} }}
          ?item rdfs:label ?label . FILTER(LANG(?label) = "{lang}")
          {region}
        }}""")
    by_item = {}
    for r in sorted(labels, key=lambda r: (r["item"], r["label"], r.get("region", ""))):
        if lang == "sr":
            # Serbian labels on Wikidata are in either script: a Latin one is turned into Cyrillic.
            r = dict(r, **{k: romanize.serbian_cyrillic(v) or v for k, v in r.items()
                          if k in ("label", "region") and not any("\u0400" <= c <= "\u04ff" for c in v)})
        by_item.setdefault(r["item"], r)
    out, names = [], set()
    for item in sorted(pops, key=lambda i: (-pops[i], i)):
        r = by_item.get(item)
        if not r or not ok(r["label"]) or r["label"] in names:
            continue
        if region_class and "region" not in r:
            continue
        city = {"name": r["label"], "weight": max(1, pops[item] // 1000)}
        if region_class:
            city["region"] = r["region"]
        out.append(city)
        names.add(r["label"])
        if len(out) == limit:
            break
    return out


def regions(cities_):
    """[[region, weight]] of the regions the cities lie in, by their population."""
    totals = {}
    for c in cities_:
        if "region" in c:
            totals[c["region"]] = totals.get(c["region"], 0) + c["weight"]
    return [[r, w] for r, w in sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))]

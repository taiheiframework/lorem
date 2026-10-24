"""The words of a language's text: the most frequent single words of its Tatoeba sentences
(CC BY 2.0 FR), filtered, with integer weights from their counts. No sentence, and no span of
more than one word, is kept."""

import collections
import math
import re
import unicodedata

from common import fetch, read_bz2_lines
import segment

# Tatoeba's weekly per-language exports. The download date and SHA-256 of each file are in
# sources.lock.json.
TATOEBA = "https://downloads.tatoeba.org/exports/per_language/{0}/{0}_sentences.tsv.bz2"

# The LDNOOBW lists (CC BY 4.0) at a fixed commit: used here only to remove words, never
# committed or shipped. Six of the 25 languages have no list there (vi, uk, bg, sr, el, he).
LDNOOBW_COMMIT = "5faf2ba42d7b1c0977169ec3611df25a3c08eb13"
LDNOOBW = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/{}/{}"
LDNOOBW_FILE = {"en": "en", "nl": "nl", "fr": "fr", "de": "de", "es": "es", "it": "it", "pt": "pt",
                "pl": "pl", "tr": "tr", "hu": "hu", "ru": "ru", "ar": "ar", "hi": "hi", "th": "th",
                "zh-Hans": "zh", "zh-Hant": "zh", "ja": "ja", "ko": "ko"}

# Tatoeba's sentences keep returning to a small cast of characters. In a cased script the
# proper-noun rule removes them; in the others they would rank as words, so they are removed by
# name, together with every given and family name of the language (names.py).
CAST = {"Tom", "Mary", "John", "Jack", "Ken", "Mike", "Bob", "Jim", "Tony", "Bill", "Paul", "Jane",
        "Alice", "Lucy", "Emily", "Ziri", "Rima", "Sami", "Layla", "Fadil", "Dania", "Yanni", "Skura",
        "Mennad", "Baya", "Tatoeba", "Muiriel", "London", "Boston", "Tokyo", "Paris", "John"}

# The same cast in the uncased scripts, which no case rule can find.
CAST_NATIVE = {
    "ja": {"トム", "メアリー", "メアリ", "ジョン", "ケン", "ジャック", "ボブ", "マイク", "アリス", "ルーシー", "ポール"},
    "zh-Hans": {"汤姆", "玛丽", "约翰", "杰克", "迈克", "肯", "鲍勃", "爱丽丝", "露西"},
    "zh-Hant": {"湯姆", "瑪麗", "約翰", "傑克", "邁克", "肯", "鮑勃", "愛麗絲", "露西"},
    "ko": {"톰", "톰은", "톰이", "톰을", "톰의", "톰에게", "메리", "메리는", "메리가", "존", "잭"},
    "th": {"ทอม", "แมรี่", "แมรี", "จอห์น", "แจ็ค", "ไมค์"},
    "ar": {"توم", "ماري", "جون", "جاك", "سامي", "ليلى", "فاضل", "زيري", "ريما", "ياني", "يني", "ريمة", "مناد", "بايا", "سكورا", "دانيا"},
    "he": {"טום", "תום", "מרי", "מריה", "במרי", "בטום", "ג'ון", "ג׳ון", "ג'ק", "סמי", "לילה"},
    "hi": {"टॉम", "मैरी", "जॉन", "जैक", "सामी", "लैला"},
}

# Words that reflect what some of Tatoeba's sentences argue about rather than the language.
TOPICAL = {"ar": {"الإنفصاليون", "الانفصاليون", "الإنفصاليين", "الانفصاليين"},
           "it": {"costruire", "nazionalità"}, "bg": {"френски"}}

# Hebrew and Arabic write a one-letter word (and, the, to, from, that) onto the next one, so a
# name of the cast also stands behind such a prefix (לתום, لتوم); German adds an s for the
# genitive (Toms). Not the Hebrew ב (in): בתום is "at the end of".
PREFIXES = {"he": "והכלמש", "ar": "وبلفك"}
GENITIVE = {"de": "s"}

# Japanese segments split inflections into pieces of a kana or two; a word that starts with a
# small kana, ん or ー is such a piece, and a single hiragana is one unless it is a particle.
JA_PARTICLES = set("はがをにのでとへもやかよねな")
JA_NO_START = set("ぁぃぅぇぉっゃゅょゎんァィゥェォッャュョヮンー")


def _ja_piece(token):
    return token[0] in JA_NO_START or (len(token) == 1 and "\u3041" <= token <= "\u3096" and token not in JA_PARTICLES)


SCRIPT_WORDS = {
    "Latn": ("LATIN",), "Cyrl": ("CYRILLIC",), "Grek": ("GREEK",), "Arab": ("ARABIC",),
    "Hebr": ("HEBREW",), "Deva": ("DEVANAGARI",), "Thai": ("THAI",),
    "Hans": ("CJK UNIFIED IDEOGRAPH",), "Hant": ("CJK UNIFIED IDEOGRAPH",),
    "Jpan": ("CJK UNIFIED IDEOGRAPH", "HIRAGANA", "KATAKANA"), "Kore": ("HANGUL",),
}
CASED = {"Latn", "Cyrl", "Grek"}
SEGMENTED = {"Hans", "Hant", "Jpan", "Thai"}


def in_script(token, script):
    """Every character a letter of the script, or a combining mark."""
    names = SCRIPT_WORDS[script]
    for ch in token:
        cat = unicodedata.category(ch)
        if cat.startswith("M"):
            continue
        if not cat.startswith("L"):
            return False
        name = unicodedata.name(ch, "")
        if not any(n in name for n in names):
            return False
    return True


def lower(word, tag):
    if tag == "tr":
        word = word.replace("I", "ı").replace("İ", "i")
    return word.lower()


def badwords(tag):
    file = LDNOOBW_FILE.get(tag)
    if not file:
        return set()
    path = fetch(f"ldnoobw-{LDNOOBW_COMMIT[:12]}/{file}", LDNOOBW.format(LDNOOBW_COMMIT, file))
    return {unicodedata.normalize("NFC", l.strip()) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()}


def sentences(conf, tag):
    code = conf["tatoeba"]
    path = fetch(f"tatoeba/{code}_sentences.tsv.bz2", TATOEBA.format(code))
    for line in read_bz2_lines(path):
        parts = line.split("\t")
        if len(parts) >= 3:
            yield unicodedata.normalize("NFC", parts[2])


APOSTROPHES = "'\u2019\u02bc"


def _runs(sentence):
    """Runs of letters, combining marks (Arabic harakat, Devanagari matras), digits, underscores
    and apostrophes: a run that holds a digit or an underscore ("5th") is not a word, and neither
    is any part of it."""
    run = []
    for ch in sentence + " ":
        cat = unicodedata.category(ch)
        if cat[0] in "LMN" or ch == "_" or ch in APOSTROPHES:
            run.append(ch)
        elif run:
            yield "".join(run)
            run = []


# Words a language capitalises wherever they stand, which the proper-noun rule would drop.
ALWAYS_CAPITALISED = {"en": {"i": "I"}}


def tokens_of(sentence, conf, tag):
    if conf["script"] in SEGMENTED:
        return None
    out = []
    for t in _runs(sentence):
        t = t.strip("'\u2019\u02bc")
        if not t or any(c.isdigit() or c == "_" for c in t):
            continue
        if any(a in t for a in "’'ʼ"):
            # An apostrophe is part of a Ukrainian word (п'ять); elsewhere it marks an elision or
            # a possessive, whose parts are not words of their own.
            if tag != "uk":
                continue
            t = t.replace("'", "’").replace("ʼ", "’")
        out.append(t)
    return out


def words(tag, conf, names, script_filter=None, limit=1300):
    """[[word, weight]], the `limit` most frequent words, most frequent first."""
    script = conf["script"]
    cased = script in CASED
    bad = badwords(tag)
    excluded = set(names) | CAST | CAST_NATIVE.get(tag, set()) | TOPICAL.get(tag, set())
    total = collections.Counter()
    non_initial = collections.Counter()
    non_initial_lower = collections.Counter()
    surfaces = collections.defaultdict(collections.Counter)

    sents = [s for s in sentences(conf, tag) if script_filter is None or script_filter(s)]
    if script in SEGMENTED:
        tokenized = segment.words(sents, conf["cldr"] if script != "Jpan" else "ja")
    else:
        tokenized = (tokens_of(s, conf, tag) for s in sents)
    for toks in tokenized:
        toks = [t for t in toks if in_script(t.replace("’", ""), script)]
        for i, t in enumerate(toks):
            key = lower(t, tag) if cased else t
            total[key] += 1
            if i > 0:
                non_initial[key] += 1
                surfaces[key][t] += 1
                if t == key:
                    non_initial_lower[key] += 1

    def bare(word):
        # Arabic vowel marks (harakat, shadda) do not make another word: الإنفصاليّون is
        # الإنفصاليون.
        return "".join(c for c in word if not unicodedata.combining(c)) if script == "Arab" else word

    excluded = excluded | {bare(n) for n in excluded}
    cast = CAST | CAST_NATIVE.get(tag, set())
    excluded |= {p + n for n in cast for p in PREFIXES.get(tag, "")}
    excluded |= {n + GENITIVE[tag] for n in cast | set(names)} if tag in GENITIVE else set()
    lowered_names = {lower(n, tag) for n in excluded} if cased else excluded
    ranked = []
    for key, count in total.most_common():
        if key in lowered_names or bare(key) in lowered_names or key in bad or lower(key, tag) in bad:
            continue
        if tag == "ja" and _ja_piece(key):
            continue
        if script in SEGMENTED and any(len(b) >= 2 and b in key for b in bad):
            continue
        form = key
        keep = ALWAYS_CAPITALISED.get(tag, {})
        if key in keep:
            ranked.append((keep[key], count))
            if len(ranked) == limit:
                break
            continue
        if cased:
            seen = non_initial[key]
            if seen == 0:
                continue
            if tag == "de":
                # German capitalises nouns: keep the form a word has inside a sentence.
                form = surfaces[key].most_common(1)[0][0]
                if len(form) > 1 and form.upper() == form:
                    continue
            elif non_initial_lower[key] * 2 < seen:
                continue  # a proper noun: capitalised inside sentences
        ranked.append((form, count))
        if len(ranked) == limit:
            break
    # Square roots flatten the curve, so that the commonest words do not crowd out the rest.
    return [[w, max(1, round(math.sqrt(c)))] for w, c in ranked]


def capitals(tag, words_):
    """[[initial, capital]] for each initial the words use, computed here so that no platform
    case mapping is needed at run time."""
    out = {}
    for w in words_:
        if tag == "nl" and w.startswith("ij"):
            out["ij"] = "IJ"
            continue
        first = w[0]
        if tag == "tr" and first == "i":
            out[first] = "İ"
            continue
        cap = first.upper()
        if len(cap) == 1 and cap != first:
            out[first] = cap
    return [[k, out[k]] for k in sorted(out)]

"""The Unicode Han Database, Unihan 16.0.0 (Unicode License v3): Mandarin readings for the pinyin
of Chinese family names (kMandarin, tone marks removed), and the simplified and traditional
variants, used only to tell Tatoeba's Simplified sentences from its Traditional ones."""

import functools
import io
import unicodedata
import zipfile

from common import fetch

VERSION = "16.0.0"
URL = f"https://www.unicode.org/Public/{VERSION}/ucd/Unihan.zip"

# Where kMandarin's most common reading is not the one a family name takes.
SURNAME_READINGS = {"单": "Shan", "解": "Xie", "仇": "Qiu", "区": "Ou", "朴": "Piao", "查": "Zha",
                    "盖": "Ge", "曾": "Zeng", "单于": "Chanyu", "尉迟": "Yuchi", "万俟": "Moqi",
                    "长孙": "Zhangsun", "乐": "Yue", "缪": "Miao", "覃": "Qin", "种": "Chong", "纪": "Ji",
                    "柏": "Bai", "繁": "Po", "秘": "Bi", "召": "Shao", "谌": "Chen", "黑": "He", "员": "Yun"}


@functools.cache
def _fields(name):
    path = fetch(f"unihan-{VERSION}/Unihan.zip", URL)
    out = {}
    with zipfile.ZipFile(path) as z:
        for member in z.namelist():
            for line in io.TextIOWrapper(z.open(member), encoding="utf-8"):
                if line.startswith("U+"):
                    cp, field, value = line.rstrip("\n").split("\t", 2)
                    if field == name:
                        out[chr(int(cp[2:], 16))] = value
    return out


def _variants(field):
    return {c: {chr(int(v.split("<")[0][2:], 16)) for v in value.split()} for c, value in _fields(field).items()}


@functools.cache
def _only():
    """The characters that exist in one of the two standards only: traditional ones that have a
    different simplified form, and simplified ones that have a different traditional form."""
    simp = _variants("kSimplifiedVariant")
    trad = _variants("kTraditionalVariant")
    traditional_only = {c for c, vs in simp.items() if vs - {c}}
    simplified_only = {c for c, vs in trad.items() if vs - {c}}
    return simplified_only - traditional_only, traditional_only - simplified_only


def is_simplified(sentence):
    s, t = _only()
    return any(c in s for c in sentence) and not any(c in t for c in sentence)


def is_traditional(sentence):
    s, t = _only()
    return any(c in t for c in sentence) and not any(c in s for c in sentence)


def pinyin(chars, surname=True):
    """The pinyin of a family name (or with surname=False any name, by the most common readings),
    without tone marks, capitalised: 王 is Wang, 欧阳 Ouyang."""
    if surname and chars in SURNAME_READINGS:
        return SURNAME_READINGS[chars]
    readings = _fields("kMandarin")
    parts = []
    for c in chars:
        if surname and c in SURNAME_READINGS:
            parts.append(SURNAME_READINGS[c].lower())
            continue
        if c not in readings:
            return None
        r = readings[c].split()[0]
        # The tone marks go; the diaeresis of ü stays, for the rule below.
        tones = {"\u0300", "\u0301", "\u0304", "\u030c"}
        plain = unicodedata.normalize("NFC", "".join(ch for ch in unicodedata.normalize("NFD", r) if ch not in tones))
        # ü is yu after l and n, as Chinese passports write it (吕 is Lyu); u elsewhere.
        parts.append(plain.replace("lü", "lyu").replace("nü", "nyu").replace("ü", "u"))
    s = "".join(parts)
    return s[:1].upper() + s[1:]

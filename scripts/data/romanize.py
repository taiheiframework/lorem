"""Romanisation by rule, written for this library, for the data scripts only: ICAO 9303 for
Cyrillic, ELOT 743 for Greek, Revised Romanization for Hangul, a passport form of Hepburn for
Japanese, and ASCII folding of Latin script. The library itself transliterates nothing at run
time: the forms are computed here and stored in the data."""

import unicodedata

# ICAO Doc 9303, part 3, Cyrillic to Latin (machine-readable zone transliteration).
ICAO = {
    "а": "a", "б": "b", "в": "v", "г": "g", "ґ": "g", "д": "d", "ђ": "d", "ѓ": "g", "е": "e",
    "ё": "e", "є": "ie", "ж": "zh", "з": "z", "ѕ": "dz", "и": "i", "і": "i", "ї": "i", "й": "i",
    "ј": "j", "к": "k", "ќ": "k", "л": "l", "љ": "lj", "м": "m", "н": "n", "њ": "nj", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "ћ": "c", "у": "u", "ў": "u", "ф": "f", "х": "kh",
    "ц": "ts", "ч": "ch", "џ": "dz", "ш": "sh", "щ": "shch", "ъ": "ie", "ы": "y", "ь": "",
    "э": "e", "ю": "iu", "я": "ia", "’": "", "'": "", "ʼ": "",
}
# Bulgarian and Serbian follow their own national systems in passports.
BULGARIAN = dict(ICAO, **{"щ": "sht", "ъ": "a", "ю": "yu", "я": "ya", "й": "y", "ж": "zh", "ц": "ts", "х": "h"})
SERBIAN = dict(ICAO, **{"ђ": "dj", "ж": "z", "ћ": "c", "ч": "c", "џ": "dz", "ш": "s", "х": "h", "ц": "c", "љ": "lj", "њ": "nj", "ј": "j"})
UKRAINIAN = dict(ICAO, **{"г": "h", "и": "y", "і": "i", "ї": "i", "й": "i", "х": "kh", "є": "ie", "ю": "iu", "я": "ia"})


def _map(text, table):
    out = []
    for ch in text:
        lower = ch.lower()
        if lower in table:
            r = table[lower]
            out.append(r[:1].upper() + r[1:] if ch != lower and r else r)
        else:
            out.append(ch)
    return "".join(out)


def cyrillic(text, tag):
    table = {"bg": BULGARIAN, "sr-Cyrl": SERBIAN, "uk": UKRAINIAN}.get(tag, ICAO)
    return _map(text, table)


# ELOT 743 (ISO 843), simplified: no diaeresis or accents are kept.
GREEK_PAIRS = {"αι": "ai", "ει": "ei", "οι": "oi", "ου": "ou", "αυ": "av", "ευ": "ev", "ηυ": "iv",
               "μπ": "mp", "ντ": "nt", "γκ": "gk", "γγ": "ng", "γξ": "nx", "γχ": "nch", "τσ": "ts", "τζ": "tz"}
GREEK = {"α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "i", "θ": "th", "ι": "i",
         "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o", "π": "p", "ρ": "r", "σ": "s",
         "ς": "s", "τ": "t", "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o"}


def greek(text):
    plain = "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))
    out, i = [], 0
    while i < len(plain):
        pair = plain[i:i + 2]
        lower = pair.lower()
        if lower in GREEK_PAIRS:
            r = GREEK_PAIRS[lower]
            out.append(r.capitalize() if pair[0] != pair[0].lower() else r)
            i += 2
            continue
        ch = plain[i]
        r = GREEK.get(ch.lower())
        out.append(ch if r is None else (r.capitalize() if ch != ch.lower() else r))
        i += 1
    return "".join(out)


FOLD = {"ß": "ss", "ł": "l", "Ł": "L", "đ": "d", "Đ": "D", "ı": "i", "ø": "o", "Ø": "O", "æ": "ae",
        "Æ": "Ae", "œ": "oe", "Œ": "Oe", "þ": "th", "Þ": "Th", "ð": "d", "Ð": "D", "ħ": "h"}


def ascii_fold(text):
    """Latin script without diacritics: é to e, ß to ss, ł to l, ı to i."""
    text = "".join(FOLD.get(c, c) for c in text)
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))


def passport_hepburn(text):
    """Hepburn as Japanese passports write it: no macrons (ō to o, ū to u), no apostrophe
    (Shin'ichi is Shinichi)."""
    plain = text.replace("ō", "o").replace("Ō", "O").replace("ū", "u").replace("Ū", "U")
    return ascii_fold(plain.replace("'", "").replace("’", ""))


def hiragana_to_katakana(text):
    return "".join(chr(ord(c) + 0x60) if "ぁ" <= c <= "ゖ" else c for c in text)


KANA = {
    "kya": "キャ", "kyu": "キュ", "kyo": "キョ", "sha": "シャ", "shu": "シュ", "sho": "ショ", "cha": "チャ",
    "chu": "チュ", "cho": "チョ", "nya": "ニャ", "nyu": "ニュ", "nyo": "ニョ", "hya": "ヒャ", "hyu": "ヒュ",
    "hyo": "ヒョ", "mya": "ミャ", "myu": "ミュ", "myo": "ミョ", "rya": "リャ", "ryu": "リュ", "ryo": "リョ",
    "gya": "ギャ", "gyu": "ギュ", "gyo": "ギョ", "ja": "ジャ", "ju": "ジュ", "jo": "ジョ", "bya": "ビャ",
    "byu": "ビュ", "byo": "ビョ", "pya": "ピャ", "pyu": "ピュ", "pyo": "ピョ", "shi": "シ", "chi": "チ",
    "tsu": "ツ", "ka": "カ", "ki": "キ", "ku": "ク", "ke": "ケ", "ko": "コ", "sa": "サ", "su": "ス",
    "se": "セ", "so": "ソ", "ta": "タ", "te": "テ", "to": "ト", "na": "ナ", "ni": "ニ", "nu": "ヌ",
    "ne": "ネ", "no": "ノ", "ha": "ハ", "hi": "ヒ", "fu": "フ", "he": "ヘ", "ho": "ホ", "ma": "マ",
    "mi": "ミ", "mu": "ム", "me": "メ", "mo": "モ", "ya": "ヤ", "yu": "ユ", "yo": "ヨ", "ra": "ラ",
    "ri": "リ", "ru": "ル", "re": "レ", "ro": "ロ", "wa": "ワ", "ga": "ガ", "gi": "ギ", "gu": "グ",
    "ge": "ゲ", "go": "ゴ", "za": "ザ", "ji": "ジ", "zu": "ズ", "ze": "ゼ", "zo": "ゾ", "da": "ダ",
    "de": "デ", "do": "ド", "ba": "バ", "bi": "ビ", "bu": "ブ", "be": "ベ", "bo": "ボ", "pa": "パ",
    "pi": "ピ", "pu": "プ", "pe": "ペ", "po": "ポ", "a": "ア", "i": "イ", "u": "ウ", "e": "エ", "o": "オ",
}


def hepburn_to_katakana(romaji):
    """The katakana of a Hepburn romanisation, or None when it is not one. A long ō is オウ, and
    オオ at the start of a name (Ōno is おおの, Satō is さとう)."""
    s = romaji.lower().replace("’", "'")
    s = ("oo" + s[1:]) if s.startswith("ō") else s
    s = s.replace("ō", "ou").replace("ū", "uu").replace("ā", "aa").replace("ē", "ee").replace("ī", "ii")
    out, i = [], 0
    while i < len(s):
        if s[i] == "'":
            i += 1
            continue
        if s[i] == "n" and (i + 1 == len(s) or s[i + 1] not in "aiueoy"):
            out.append("ン")
            i += 1
            continue
        if i + 1 < len(s) and s[i] == s[i + 1] and s[i] not in "aiueon":
            out.append("ッ")
            i += 1
            continue
        if s[i] == "t" and s[i + 1:i + 3] == "ch":
            out.append("ッ")
            i += 1
            continue
        for size in (3, 2, 1):
            part = s[i:i + size]
            if part in KANA:
                out.append(KANA[part])
                i += size
                break
        else:
            return None
    return "".join(out)


# Revised Romanization of Korean, by syllable: initial, medial and final jamo.
RR_INITIAL = ["g", "kk", "n", "d", "tt", "r", "m", "b", "pp", "s", "ss", "", "j", "jj", "ch", "k", "t", "p", "h"]
RR_MEDIAL = ["a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe", "yo", "u", "wo", "we", "wi",
             "yu", "eu", "ui", "i"]
RR_FINAL = ["", "k", "k", "k", "n", "n", "n", "t", "l", "k", "m", "l", "l", "l", "p", "l", "m", "p", "p", "t",
            "t", "ng", "t", "t", "k", "t", "p", "t"]


def hangul(text):
    out = []
    for ch in text:
        code = ord(ch) - 0xAC00
        if 0 <= code < 11172:
            out.append(RR_INITIAL[code // 588] + RR_MEDIAL[(code % 588) // 28] + RR_FINAL[code % 28])
        else:
            out.append(ch)
    s = "".join(out)
    return s[:1].upper() + s[1:]


# Serbian writes the same alphabet in Latin and Cyrillic, letter for letter (Gaj's Latin and
# Vuk's Cyrillic), so a Latin label is turned into Cyrillic without loss.
SERBIAN_DIGRAPHS = {"lj": "љ", "nj": "њ", "dž": "џ"}
SERBIAN_LETTERS = {
    "a": "а", "b": "б", "c": "ц", "č": "ч", "ć": "ћ", "d": "д", "đ": "ђ", "e": "е", "f": "ф", "g": "г",
    "h": "х", "i": "и", "j": "ј", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "r": "р",
    "s": "с", "š": "ш", "t": "т", "u": "у", "v": "в", "z": "з", "ž": "ж",
}


def serbian_cyrillic(text):
    """The Cyrillic of a Serbian Latin text, or None when it holds a letter Serbian Latin lacks."""
    out, i = [], 0
    while i < len(text):
        two = text[i:i + 2]
        if two.lower() in SERBIAN_DIGRAPHS:
            c = SERBIAN_DIGRAPHS[two.lower()]
            out.append(c.upper() if two[0].isupper() else c)
            i += 2
            continue
        ch = text[i]
        if ch.lower() in SERBIAN_LETTERS:
            c = SERBIAN_LETTERS[ch.lower()]
            out.append(c.upper() if ch.isupper() else c)
        elif ch in " -'":
            out.append(ch)
        else:
            return None
        i += 1
    return "".join(out)

"""Address formats, postal code patterns, street patterns and phone patterns of each language's
default country, written for this library. The line order, fields and postal code shapes follow
the address metadata of Google libaddressinput (CC BY 4.0), adapted to this library's template
syntax; UPU material was a reference only.

Address lines: {street} {city} {region} {postalCode} {country}. Streets: {family} and
{familyFemale} (a family name in its male or female form; in Russian, Ukrainian and Greek the
female form is also the genitive a street name takes), {given}, {word} and {Word} (a word of the
language's text, the second capitalised), {number} (1 to 200) and {small} (1 to 30). Codes: #
a digit, N a digit 1 to 9, % a digit 2 to 9, ? an ASCII capital letter.

A phone pattern is fictional only where the country reserves the range for fiction and the
reservation is cited in docs/data-sources.md (NANP 555-0100 to 555-0199)."""

COUNTRIES = {
    "US": dict(
        lines=["{street}", "{city}, {region} {postalCode}", "{country}"], separator=", ",
        postalCode="#####", phone="+1 %## 555-01##", fictionalPhone=True,
        streets=["{number} {family} Street", "{number} {family} Avenue", "{number} {family} Road",
                 "{number} {given} Drive", "{number} Main Street", "{number} Oak Street",
                 "{number} Maple Avenue", "{number} Park Avenue", "{number} Pine Street",
                 "{number} Cedar Lane", "{number} Elm Street", "{number} Lake Drive",
                 "{number} Hill Road", "{number} Washington Street", "{number} Lincoln Avenue"]),
    "NL": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="N### ??", phone="+31 6 ########", fictionalPhone=False,
        streets=["{family}straat {number}", "{family}laan {number}", "{family}plein {small}",
                 "{family}weg {number}", "Kerkstraat {number}", "Dorpsstraat {number}",
                 "Molenweg {number}", "Stationsweg {number}", "Schoolstraat {number}",
                 "Nieuwstraat {number}", "Julianastraat {number}", "Beatrixlaan {number}"]),
    "FR": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="N####", phone="+33 N ## ## ## ##", fictionalPhone=False,
        streets=["{number} rue {given} {family}", "{number} avenue {given} {family}",
                 "{number} boulevard {family}", "{number} rue de la Gare", "{number} rue du Moulin",
                 "{number} place de l’Église", "{number} rue de la République",
                 "{number} Grande Rue", "{number} rue des Écoles", "{number} chemin des Vignes"]),
    "DE": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="#####", phone="+49 17# #######", fictionalPhone=False,
        streets=["{family}straße {number}", "{family}weg {number}", "{family}platz {small}",
                 "Hauptstraße {number}", "Schulstraße {number}", "Gartenstraße {number}",
                 "Bahnhofstraße {number}", "Dorfstraße {number}", "Bergstraße {number}",
                 "Kirchstraße {number}", "Lindenstraße {number}"]),
    "ES": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="N####", phone="+34 6## ## ## ##", fictionalPhone=False,
        streets=["Calle de {given} {family}, {number}", "Avenida de {family}, {number}",
                 "Calle Mayor, {number}", "Calle Real, {number}", "Plaza Mayor, {small}",
                 "Calle de la Iglesia, {number}", "Calle del Sol, {number}",
                 "Paseo de la Estación, {number}"]),
    "IT": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="#####", phone="+39 3## ### ####", fictionalPhone=False,
        streets=["Via {given} {family}, {number}", "Piazza {family}, {small}", "Corso {family}, {number}",
                 "Via Roma, {number}", "Via Garibaldi, {number}", "Via Mazzini, {number}",
                 "Via Cavour, {number}", "Via Dante, {number}", "Via Verdi, {number}"]),
    "BR": dict(
        lines=["{street}", "{city} - {region}", "{postalCode}", "{country}"], separator=", ",
        postalCode="#####-###", phone="+55 N# 9####-####", fictionalPhone=False,
        streets=["Rua {given} {family}, {number}", "Avenida {family}, {number}", "Rua das Flores, {number}",
                 "Rua São João, {number}", "Avenida Brasil, {number}", "Rua Sete de Setembro, {number}",
                 "Praça da Matriz, {small}", "Rua Quinze de Novembro, {number}"]),
    "PL": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="##-###", phone="+48 N## ### ###", fictionalPhone=False,
        streets=["ul. Polna {number}", "ul. Leśna {number}", "ul. Słoneczna {number}",
                 "ul. Krótka {number}", "ul. Szkolna {number}", "ul. Ogrodowa {number}",
                 "ul. Lipowa {number}", "ul. Brzozowa {number}", "ul. Łąkowa {number}",
                 "ul. Kwiatowa {number}", "ul. Kościelna {number}/{small}", "ul. Zielona {number}/{small}"]),
    "TR": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="N####", phone="+90 5## ### ## ##", fictionalPhone=False,
        streets=["{family} Sokak No: {small}", "Atatürk Caddesi No: {number}",
                 "Cumhuriyet Caddesi No: {number}", "İnönü Caddesi No: {number}",
                 "İstiklal Caddesi No: {number}", "Okul Sokak No: {small}", "Çarşı Sokak No: {small}"]),
    "VN": dict(
        lines=["{street}", "{city}", "{postalCode}", "{country}"], separator=", ",
        postalCode="N####", phone="+84 9# ### ## ##", fictionalPhone=False,
        streets=["Số {number} đường {family} {given}", "Số {number} phố {family} {given}",
                 "Số {number} đường Lê Lợi", "Số {number} đường Trần Hưng Đạo",
                 "Số {number} đường Hai Bà Trưng", "Số {number} đường Nguyễn Huệ"]),
    "HU": dict(
        lines=["{city}", "{street}", "{postalCode}", "{country}"], separator=", ",
        postalCode="N###", phone="+36 N0 ### ####", fictionalPhone=False,
        streets=["{family} utca {number}.", "{family} tér {small}.", "Kossuth Lajos utca {number}.",
                 "Petőfi Sándor utca {number}.", "Rákóczi út {number}.", "Fő utca {number}.",
                 "Ady Endre utca {number}.", "Dózsa György út {number}."]),
    "VA": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="00120", phone="+39 06 698#####", fictionalPhone=False,
        streets=["Via {familyFemale} {number}", "Via {familyFemale} {small}", "Clivus {familyFemale} {small}"]),
    "RU": dict(
        lines=["{street}", "{city}", "{postalCode}", "{country}"], separator=", ",
        postalCode="N#####", phone="+7 9## ###-##-##", fictionalPhone=False,
        streets=["ул. {familyFemale}, д. {small}", "ул. {familyFemale}, д. {small}, кв. {number}",
                 "ул. Садовая, д. {small}", "ул. Центральная, д. {small}", "ул. Школьная, д. {small}",
                 "ул. Лесная, д. {small}", "ул. Молодёжная, д. {small}", "пр. Мира, д. {small}",
                 "ул. Набережная, д. {small}"]),
    "UA": dict(
        lines=["{street}", "{city}", "{postalCode}", "{country}"], separator=", ",
        postalCode="#####", phone="+380 9# ### ## ##", fictionalPhone=False,
        streets=["вул. Шевченка, {small}", "вул. Садова, {small}", "вул. Центральна, {small}",
                 "вул. Миру, {small}", "вул. Шкільна, {small}", "вул. Лісова, {small}",
                 "вул. Набережна, {small}", "просп. Незалежності, {small}", "вул. Зелена, {small}"]),
    "BG": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="N###", phone="+359 8# ### ####", fictionalPhone=False,
        streets=["ул. „Васил Левски“ № {small}", "бул. „Христо Ботев“ № {small}",
                 "ул. „Иван Вазов“ № {small}", "ул. „Шипка“ № {small}", "ул. „Раковски“ № {small}",
                 "бул. „България“ № {small}", "ул. „Цар Симеон“ № {small}"]),
    "RS": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="N####", phone="+381 6# ### ####", fictionalPhone=False,
        streets=["Кнеза Милоша {number}", "Кнез Михаилова {number}", "Булевар краља Александра {number}",
                 "Немањина {number}", "Његошева {number}", "Цара Душана {number}",
                 "Вука Караџића {number}", "Николе Тесле {number}"]),
    "GR": dict(
        lines=["{street}", "{postalCode} {city}", "{country}"], separator=", ",
        postalCode="N## ##", phone="+30 69# ### ####", fictionalPhone=False,
        streets=["{familyFemale} {number}", "Ερμού {number}", "Πανεπιστημίου {number}", "Σταδίου {number}",
                 "Αθηνάς {number}", "Αιόλου {number}", "Πατησίων {number}", "Κηφισίας {number}"]),
    "EG": dict(
        lines=["{street}", "{city}", "{postalCode}", "{country}"], separator="، ",
        postalCode="#####", phone="+20 1# #### ####", fictionalPhone=False,
        streets=["{number} شارع {family}", "{number} شارع التحرير", "{number} شارع الهرم",
                 "{number} شارع النيل", "{number} شارع الجمهورية", "{number} شارع رمسيس",
                 "{number} شارع الثورة"]),
    "IL": dict(
        lines=["{street}", "{city} {postalCode}", "{country}"], separator=", ",
        postalCode="#######", phone="+972 5#-###-####", fictionalPhone=False,
        streets=["רחוב {family} {number}", "רחוב הרצל {number}", "שדרות רוטשילד {number}",
                 "רחוב בן יהודה {number}", "רחוב ויצמן {number}", "רחוב הנביאים {number}",
                 "רחוב יפו {number}", "רחוב אלנבי {number}"]),
    "IN": dict(
        lines=["{street}", "{city} {postalCode}", "{region}", "{country}"], separator=", ",
        postalCode="N#####", phone="+91 9#### #####", fictionalPhone=False,
        streets=["{number}, {family} मार्ग", "{number}, गांधी मार्ग", "{number}, नेहरू मार्ग",
                 "{number}, स्टेशन रोड", "{number}, मुख्य बाज़ार", "{number}, {given} नगर"]),
    "TH": dict(
        lines=["{street}", "{city} {postalCode}", "{country}"], separator=" ",
        postalCode="N####", phone="+66 8# ### ####", fictionalPhone=False,
        streets=["{number}/{small} ถนนสุขุมวิท", "{number}/{small} ถนนพหลโยธิน", "{number} ถนนเพชรบุรี",
                 "{number} ถนนสีลม", "{number} ถนนพระราม 4", "{number} ถนนรัชดาภิเษก", "{number} ถนนเจริญกรุง"]),
    "CN": dict(
        lines=["{country}", "{postalCode} {city}", "{street}"], separator=" ",
        postalCode="N#####", phone="+86 1## #### ####", fictionalPhone=False,
        streets=["人民路{number}号", "中山路{number}号", "解放路{number}号", "建设路{number}号", "和平路{number}号",
                 "新华路{number}号", "长江路{number}号", "黄河路{number}号", "胜利路{number}号", "文化路{number}号",
                 "朝阳路{number}号", "青年路{number}号"]),
    "TW": dict(
        lines=["{country}", "{postalCode} {city}", "{street}"], separator=" ",
        postalCode="N##", phone="+886 9## ### ###", fictionalPhone=False,
        streets=["中山路{number}號", "中正路{number}號", "民生路{number}號", "民權路{number}號", "民族路{number}號",
                 "復興路{number}號", "忠孝東路{number}號", "仁愛路{number}號", "信義路{number}號", "和平東路{number}號"]),
    "JP": dict(
        lines=["{country}", "〒{postalCode}", "{city}{street}"], separator=" ",
        postalCode="###-####", phone="+81 90-####-####", fictionalPhone=False,
        streets=["{family}{small}-{small}-{small}", "{family}町{small}-{small}", "本町{small}-{small}-{small}",
                 "中央{small}-{small}-{small}", "栄町{small}-{small}"]),
    "KR": dict(
        lines=["{country}", "{city} {street}", "{postalCode}"], separator=" ",
        postalCode="#####", phone="+82 10-####-####", fictionalPhone=False,
        streets=["세종대로 {number}", "테헤란로 {number}", "을지로 {number}", "종로 {number}", "강남대로 {number}",
                 "한강대로 {number}", "중앙로 {number}", "시청로 {number}"]),
}

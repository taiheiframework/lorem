package dev.taihei.mihon

import java.time.*

import zio.test.*

import dev.taihei.tsuji.Language

object SeededSpec extends ZIOSpecDefault:

  private val noon  = Instant.parse("2026-10-24T12:00:00Z")
  private val clock = Clock.fixed(noon, ZoneOffset.UTC)

  // A run of draws in one language, so a test compares whole sequences and not one value.
  private def run(mihon: Mihon): List[String] =
    val p = mihon.person
    List(
      mihon.sentence,
      p.fullName,
      p.latin,
      p.reading.getOrElse("-"),
      mihon.email,
      mihon.address.singleLine,
      mihon.phone,
      mihon.title,
      mihon.word,
    )

  // The values of seed 42 in each language in this version. They are the same on the JVM and on
  // Scala.js, which this test proves by running on both. A change to the data or to how a
  // generator draws changes them: update them in that change, and say so in the release notes.
  private val golden: Map[String, List[String]] = Map(
    "ar" -> List(
      "سكورة ذلك بعد وجدت علاقة له نستطيع بارد من كان كانت متن؟",
      "شريفة أمين",
      "Sherifa Amin",
      "-",
      "ahmad.el.gendy@lunarbytefusion.example",
      "180 شارع الثورة، ديروط، 77233، مصر",
      "+20 15 3754 7573",
      "عدة وقت خائف أسكن",
      "العديد",
    ),
    "bg" -> List(
      "Знаете сняг но съм стана в много види мисля трябваше казвам знаех?",
      "Весела Христова",
      "Vesela Hristova",
      "-",
      "ivan.ivanov@lunarbytefusion.example",
      "ул. „Васил Левски“ № 25, 3723 Пловдив, България",
      "+359 89 537 5475",
      "Вашият нямам ужасно",
      "дойда",
    ),
    "de" -> List(
      "Rede seinen Schuld leider hätte dabei kommt war spricht geht tatsächlich Abend?",
      "Ute Winter",
      "Ute Winter",
      "-",
      "ulrich.meier@lunarbytefusion.example",
      "Schulstraße 180, 77233 Frankfurt am Main, Deutschland",
      "+49 175 3754757",
      "Habt ganze Wohnung schwierig",
      "leihen",
    ),
    "el" -> List(
      "Διαμέρισμα τελειώσει δασκάλα ζήτησα μια μείνω μου πιο σχολείο ακόμα πίσω τι;",
      "Ανδρομάχη Σταμούλη",
      "Andromachi Stamouli",
      "-",
      "giannis.nikolaidis@lunarbytefusion.example",
      "Πανεπιστημίου 180, 372 33 Βόλος, Ελλάδα",
      "+30 695 375 4757",
      "Όλων καταλαβαίνω γλώσσα γλυκό",
      "μένα",
    ),
    "en" -> List(
      "Few now own a too dead taking cars let nature his within?",
      "Virginia Wood",
      "Virginia Wood",
      "-",
      "charles.white@lunarbytefusion.example",
      "180 Cedar Lane, Greensboro, North Carolina 77233, United States",
      "+1 737 555-0154",
      "Cold Set Even",
      "today",
    ),
    "es" -> List(
      "¿Arroz larga nadar conseguir chica parar es verdad otras vuelto a lo?",
      "Aina López",
      "Aina López",
      "-",
      "manuel.garcia@lunarbytefusion.example",
      "Calle Mayor, 180, 37233 Madrid, España",
      "+34 653 75 47 57",
      "Accidente número que colores",
      "conoce",
    ),
    "fr" -> List(
      "Raison sortir voie demain et pour préparé dire et bleu venu vous ?",
      "Isabelle Hubert",
      "Isabelle Hubert",
      "-",
      "alain.duval@lunarbytefusion.example",
      "180 rue du Moulin, 37233 Nîmes, France",
      "+33 5 37 54 75 73",
      "Étaient français kabyles il",
      "aimé",
    ),
    "he" -> List(
      "לנסות נתנה עם יכולה כולם סוג איך לעזור מודאג ככל עייף לא?",
      "סימה לביא",
      "Sima Lavi",
      "-",
      "dov.harpaz@lunarbytefusion.example",
      "רחוב הנביאים 24, פתח תקווה 7723349, ישראל",
      "+972 57-547-5733",
      "שלי",
      "אתה",
    ),
    "hi" -> List(
      "तुम पता समय घर ध्यान वकील बिलकुल मिलेगा रखा चार मतलब रूस?",
      "जानकी सिंह",
      "Janaki Singh",
      "-",
      "ajay.reddy@lunarbytefusion.example",
      "66, ऋचा नगर, मुम्बई 372334, महाराष्ट्र, भारत",
      "+91 95475 73308",
      "उन्हें कपड़े",
      "हुआ",
    ),
    "hu" -> List(
      "Jött el elé húsz amerikai venni rá legyen ezek járni úgy alig?",
      "Hajdú Eszter",
      "Hajdú Eszter",
      "-",
      "acs.gyula@lunarbytefusion.example",
      "Budapest, Rákóczi út 165., 3723, Magyarország",
      "+36 60 537 5475",
      "Ti tudsz elégedett",
      "lennie",
    ),
    "it" -> List(
      "Diverso informazioni un spazio mai terra sarò guidare nostra cinque caldo in?",
      "Francesca Rizzo",
      "Francesca Rizzo",
      "-",
      "marco.bianchi@lunarbytefusion.example",
      "Via Roma, 180, 77233 Verona, Italia",
      "+39 353 754 7573",
      "Stavo frasi mal volte",
      "musica",
    ),
    "ja" -> List(
      "失敗ない歩くテレビの眠クリスマスせんなか力経験。",
      "奥田ゆり",
      "Okuda Yuri",
      "オクダ ユリ",
      "morita.hiroko@lunarbytefusion.example",
      "日本 〒057-7233 市原市栄町30-26",
      "+81 90-3754-7573",
      "よ流れ家やる",
      "なら",
    ),
    "ko" -> List(
      "네 해서 싶습니다 톰과 샀어요 이것은 아무도 것이 찾았다 했는데 커피를 일한다?",
      "박영희",
      "Park Yeong-hui",
      "-",
      "ko.hyeon-seok@lunarbytefusion.example",
      "대한민국 청주시 을지로 180 77233",
      "+82 10-5375-4757",
      "좋지 오늘 아니야 있다는",
      "있어",
    ),
    "la" -> List(
      "Quas rutrum ferri amet eloquentiam sanctus lorem mollis referrentur habitasse graecis alterum?",
      "Publia Sulpicia",
      "Publia Sulpicia",
      "-",
      "gnaeus.tullius@lunarbytefusion.example",
      "Clivus Pompeia 13, 00120 Civitas Vaticana, Civitas Vaticana",
      "+39 06 69833495",
      "Suavitate vituperata noluisse efficiantur",
      "inceptos",
    ),
    "nl" -> List(
      "Je ziet twaalf vinden gelooft gek jullie beetje dicht gebroken de verschrikkelijk?",
      "Kirsten Koopmans",
      "Kirsten Koopmans",
      "-",
      "robin.de.vries@lunarbytefusion.example",
      "Beatrixlaan 66, 3723 PK Apeldoorn, Nederland",
      "+31 6 37547573",
      "Valt hele zij helemaal",
      "gaat",
    ),
    "pl" -> List(
      "Są więc iść minut tobą jesteście lekarz kto nią przyszedł najpierw piękne?",
      "Agnieszka Jakubowska",
      "Agnieszka Jakubowska",
      "-",
      "marek.baran@lunarbytefusion.example",
      "ul. Polna 180, 77-233 Łódź, Polska",
      "+48 537 547 573",
      "Lubię miesiącu miasta wróci",
      "ciągle",
    ),
    "pt" -> List(
      "Terra perguntas país ao tarde pequeno talvez pedido pai indo conte algo?",
      "Alexandra Silva",
      "Alexandra Silva",
      "-",
      "helio.santos@lunarbytefusion.example",
      "Avenida Brasil, 138, Duque de Caxias - Rio de Janeiro, 77233-495, Brasil",
      "+55 64 97573-3086",
      "Algo",
      "para",
    ),
    "ru" -> List(
      "Её этим его принёс дождь отвечать что идти умеешь прийти друзья твоих?",
      "Людмила Макарова",
      "Liudmila Makarova",
      "-",
      "aleksandr.zhukov@lunarbytefusion.example",
      "ул. Лесная, д. 26, Чита, 372334, Россия",
      "+7 937 547-57-33",
      "Говорите",
      "хочет",
    ),
    "sr-Cyrl" -> List(
      "Отишла како пут мама они су осећам волео лето познајеш кошта одакле?",
      "Јелена Симић",
      "Jelena Simic",
      "-",
      "branko.jovanovic@lunarbytefusion.example",
      "Булевар краља Александра 180, 37233 Крагујевац, Србија",
      "+381 65 375 4757",
      "Каже свом победио њим",
      "људи",
    ),
    "th" -> List(
      "ฉันใช่พูดหิมะบนคันห้องลับสิบพรุ่งกว้าง",
      "ภัทรสุดา ทองเดชศรี",
      "Pattarasuda Thongdejsri",
      "-",
      "yanisa.chochuwong@lunarbytefusion.example",
      "114 ถนนรัชดาภิเษก นนทบุรี 35772 ไทย",
      "+66 84 953 7547",
      "กระจก",
      "ผม",
    ),
    "tr" -> List(
      "Başladı boyunca not etti kez kitap dakika hâlâ eminim yaptığını yapmak gerekiyordu?",
      "Gizem Özkan",
      "Gizem Özkan",
      "-",
      "yasar.erdogan@lunarbytefusion.example",
      "Çarşı Sokak No: 30, 37233 Çerkezköy, Türkiye",
      "+90 553 754 75 73",
      "En söylediler yatakta anlama",
      "adı",
    ),
    "uk" -> List(
      "Прийти вивчити має на концерт нього книжка стільки дай було сьогодні говорили?",
      "Вікторія Ісаєнко",
      "Viktoriia Isaienko",
      "-",
      "vadym.bondarenko@lunarbytefusion.example",
      "вул. Миру, 30, Одеса, 77233, Україна",
      "+380 95 375 47 57",
      "Школи без це така",
      "усіх",
    ),
    "vi" -> List(
      "Như bạn người thách nhận tồi tấm thể súng chối hay thị?",
      "Nguyễn Xuân",
      "Nguyễn Xuân",
      "-",
      "huynh.claude@lunarbytefusion.example",
      "Số 180 đường Phạm Tuyết, Nha Trang, 37233, Việt Nam",
      "+84 95 475 73 30",
      "Cà đã không nói",
      "tòa",
    ),
    "zh-Hans" -> List(
      "的照顾个还是但是不同都在房吧啦空。",
      "李佳欣",
      "Li Jiaxin",
      "-",
      "chen.dan@lunarbytefusion.example",
      "中国 357723 无锡市 中山路165号",
      "+86 195 3754 7573",
      "兄弟事年看法",
      "与",
    ),
    "zh-Hant" -> List(
      "他考慮第一嘗試員鳥上有他我將在啊。",
      "洪秋鸞",
      "Hong Qiuluan",
      "-",
      "ma.suzhen@lunarbytefusion.example",
      "台灣 357 竹北市 仁愛路13號",
      "+886 933 495 375",
      "甚至中文眼睛裏請",
      "慢",
    ),
  )

  def spec = suite("SeededSpec")(
    test("every language has its golden run") {
      assertTrue(golden.keySet == Mihon.languages.map(_.tag).toSet)
    },
    suite("seed 42 gives these values, on every platform")(
      golden.toSeq.sortBy(_._1).map((tag, values) =>
        test(tag)(assertTrue(run(Mihon.seeded(42L, Language(tag), clock)) == values))
      )*
    ),
    test("the same seed and language give the same values") {
      assertTrue(run(Mihon.seeded(7L, Language("ja"))) == run(Mihon.seeded(7L, Language("ja"))))
    },
    test("another seed gives other values") {
      assertTrue(run(Mihon.seeded(7L)) != run(Mihon.seeded(8L)))
    },
    test("secure generators do not repeat each other") {
      assertTrue(run(Mihon.secure()) != run(Mihon.secure()))
    },
    test("withLanguage shares the generator: the views draw one sequence between them") {
      val one   = Mihon.seeded(5L, clock = clock)
      val other = one.withLanguage(Language("la"))
      val mixed = List(one.int(1000), other.int(1000), one.int(1000))
      val plain = Mihon.seeded(5L, clock = clock)
      assertTrue(
        other.language == Language("la"),
        one.language == Language.English,
        other.today == one.today,
        mixed == List(plain.int(1000), plain.int(1000), plain.int(1000)),
      )
    },
    test("a seeded run does not depend on which language the generator started in") {
      val a = Mihon.seeded(9L).withLanguage(Language("la"))
      val b = Mihon.seeded(9L, Language("la"))
      assertTrue(run(a) == run(b))
    },
  )

end SeededSpec

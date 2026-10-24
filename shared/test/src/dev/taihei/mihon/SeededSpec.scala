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
      "قل مهمة الجزائر كما حاول تكتب الزرافات أطول الصباح نعم شعر عمله؟",
      "سميرة حسن",
      "Samira Hasan",
      "-",
      "tahir.samir@lunarbytefusion.example",
      "180 شارع الثورة، السويس، 77233، مصر",
      "+20 15 3754 7573",
      "ماثيو القبائل ذاك دعونا",
      "الأصدقاء",
    ),
    "bg" -> List(
      "Някого доверие една ям беше означава мога кафето искала ме път красива?",
      "Илияна Божинова",
      "Iliyana Bozhinova",
      "-",
      "georgi.stefanov@lunarbytefusion.example",
      "ул. „Васил Левски“ № 25, 3723 Пловдив, България",
      "+359 89 537 5475",
      "Дай тя голяма",
      "искала",
    ),
    "de" -> List(
      "Wie nehme sagen ist mein was können was eigentlich lügen erste diesen?",
      "Anke Weber",
      "Anke Weber",
      "-",
      "dieter.vogt@lunarbytefusion.example",
      "Schulstraße 180, 77233 Frankfurt am Main, Deutschland",
      "+49 175 3754757",
      "Herum kaputt jemandem glaube",
      "will",
    ),
    "el" -> List(
      "Γάτα με πόσες ξέρεις γνώμη ένας ως λόγω έρθεις καθόλου πάντα είδες;",
      "Παρασκευή Αργυρού",
      "Paraskevi Argyrou",
      "-",
      "konstantinos.zervos@lunarbytefusion.example",
      "Πανεπιστημίου 180, 372 33 Δάφνη Αττικής, Ελλάδα",
      "+30 695 375 4757",
      "Βοηθήσουμε κοντά είχε πάμε",
      "πάω",
    ),
    "en" -> List(
      "Pretty has dangerous themselves color knew manager whether everything world their week?",
      "Virginia Wood",
      "Virginia Wood",
      "-",
      "charles.white@lunarbytefusion.example",
      "180 Cedar Lane, Greensboro, North Carolina 77233, United States",
      "+1 737 555-0154",
      "Safe Into Many",
      "of",
    ),
    "es" -> List(
      "¿Excelente su novela ellos encontró sé fuerte baja mañana escritorio y gente?",
      "Rosa de la Fuente",
      "Rosa de la Fuente",
      "-",
      "cristobal.mendez@lunarbytefusion.example",
      "Calle Mayor, 180, 37233 Avilés, España",
      "+34 653 75 47 57",
      "Papá más colores ayer",
      "hoy",
    ),
    "fr" -> List(
      "Impossible plan ou gouvernement mit anniversaire plutôt regarder ici posé pleine assez ?",
      "Corinne Garnier",
      "Corinne Garnier",
      "-",
      "jean.bloch@lunarbytefusion.example",
      "180 rue du Moulin, 37233 Nîmes, France",
      "+33 5 37 54 75 73",
      "Frais japonais presque chose",
      "théâtre",
    ),
    "he" -> List(
      "ממה בשקט וגם חם לגור ממך זאת אני ידי כיף איך משהו?",
      "אפרת מעוז",
      "Efrat Maoz",
      "-",
      "chagai.shapira@lunarbytefusion.example",
      "רחוב הנביאים 24, פתח תקווה 7723349, ישראל",
      "+972 57-547-5733",
      "לחלוטין",
      "הייתי",
    ),
    "hi" -> List(
      "हमने मैंने खिड़की जल्द भाषा था साल करीब इस्तेमाल बात उनके जाने?",
      "रोशनी हजारिका",
      "Roshani Hazarika",
      "-",
      "michael.sharma@lunarbytefusion.example",
      "66, मीना नगर, मुम्बई 372334, महाराष्ट्र, भारत",
      "+91 95475 73308",
      "छोड़ो ज़्यादा",
      "तुम्हारी",
    ),
    "hu" -> List(
      "Már törvény ha hát nézd busszal lánya apja de zenét el van?",
      "Kovács Anna",
      "Kovács Anna",
      "-",
      "kadar.mor@lunarbytefusion.example",
      "Budapest, Rákóczi út 165., 3723, Magyarország",
      "+36 60 537 5475",
      "Szeme voltunk keres",
      "tűnik",
    ),
    "it" -> List(
      "Erano matematica lo certo il camminare me i cucina tua faceva paio?",
      "Martina Marchi",
      "Martina Marchi",
      "-",
      "guido.tosi@lunarbytefusion.example",
      "Via Roma, 180, 77233 Verona, Italia",
      "+39 353 754 7573",
      "Minuto queste auto vorresti",
      "presidente",
    ),
    "ja" -> List(
      "よけたと国民そう人口はなるちょうど着く去年。",
      "鈴木さちこ",
      "Suzuki Sachiko",
      "スズキ サチコ",
      "sakamoto.hiroko@lunarbytefusion.example",
      "日本 〒057-7233 市原市栄町30-26",
      "+81 90-3754-7573",
      "警察両親成長なる",
      "立ち",
    ),
    "ko" -> List(
      "배우는 가득 어제 목소리가 실수를 한번 한국에 요즘 배워야 일어났다 만든다 있어서?",
      "이정은",
      "Lee Jeong-eun",
      "-",
      "choi.jung-hyun@lunarbytefusion.example",
      "대한민국 강릉시 을지로 180 77233",
      "+82 10-5375-4757",
      "딱 죽였다 아세요 문장은",
      "해줘",
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
      "Na deed verteld ga nodig eigenlijk verlegen succes men al zoals lag?",
      "Maria Schwindl",
      "Maria Schwindl",
      "-",
      "cornelis.dijkstra@lunarbytefusion.example",
      "Beatrixlaan 66, 3723 PK Apeldoorn, Nederland",
      "+31 6 37547573",
      "Plotseling land noch prachtige",
      "zelf",
    ),
    "pl" -> List(
      "Panu po wyjść mów dać został pojechał uczę kawę tylko zawsze na?",
      "Martyna Piotrowska",
      "Martyna Piotrowska",
      "-",
      "wladyslaw.nowicki@lunarbytefusion.example",
      "ul. Polna 180, 77-233 Łódź, Polska",
      "+48 537 547 573",
      "Lata mojej czy mieli",
      "iść",
    ),
    "pt" -> List(
      "Ele sempre venha tente rico gosto passei própria melhor perfeito você coisa?",
      "Antonia Dias",
      "Antonia Dias",
      "-",
      "joao.garcia@lunarbytefusion.example",
      "Avenida Brasil, 138, Camaçari - Bahia, 77233-495, Brasil",
      "+55 64 97573-3086",
      "Emprego",
      "deseja",
    ),
    "ru" -> List(
      "Страны руки кое сможешь ничего родителей понятия видел они говоря многих жениться?",
      "Евгения Жукова",
      "Evgeniia Zhukova",
      "-",
      "leonid.chernov@lunarbytefusion.example",
      "ул. Лесная, д. 26, Чита, 372334, Россия",
      "+7 937 547-57-33",
      "Взять",
      "свои",
    ),
    "sr-Cyrl" -> List(
      "Његовом ми свиђа желите даље вести смо познајем пример отвори изгубио такси?",
      "Јасна Ђурђевић",
      "Jasna Djurdjevic",
      "-",
      "ljubisa.perovic@lunarbytefusion.example",
      "Булевар краља Александра 180, 37233 Ужице, Србија",
      "+381 65 375 4757",
      "Школу ти допада хоћеш",
      "то",
    ),
    "th" -> List(
      "ฉันใช่พูดหิมะบนคันห้องลับสิบพรุ่งกว้าง",
      "เบญญาภา ไล้สวน",
      "Benyapa Laisuan",
      "-",
      "chanisa.kanlaha@lunarbytefusion.example",
      "114 ถนนรัชดาภิเษก นนทบุรี 35772 ไทย",
      "+66 84 953 7547",
      "กระจก",
      "ผม",
    ),
    "tr" -> List(
      "Olmak kolay onların işi etti olarak bisiklet sahiptir yaptığı her şey yüksek?",
      "Cansu Albayrak",
      "Cansu Albayrak",
      "-",
      "emre.cetin@lunarbytefusion.example",
      "Çarşı Sokak No: 30, 37233 İstanbul, Türkiye",
      "+90 553 754 75 73",
      "Geri en emekli işi",
      "hangisidir",
    ),
    "uk" -> List(
      "Ваш правду тато автобус тобі про познайомився мене заради обід всім двері?",
      "Орися Ковальова",
      "Orysia Kovalova",
      "-",
      "heorhii.kravchuk@lunarbytefusion.example",
      "вул. Миру, 30, Одеса, 77233, Україна",
      "+380 95 375 47 57",
      "Зовсім потрібно ненавидить трапилося",
      "довго",
    ),
    "vi" -> List(
      "Kể nhìn kinh một xin lời đi phát cũ chuẩn tích thực?",
      "Nguyễn Kim",
      "Nguyễn Kim",
      "-",
      "nguyen.phuoc@lunarbytefusion.example",
      "Số 66 đường Nguyễn Huệ, Thành phố Hồ Chí Minh, 372334, Việt Nam",
      "+84 93 754 75 73",
      "Là tới đi mỏ",
      "khởi",
    ),
    "zh-Hans" -> List(
      "之一让确定进来人东西里面耐心学习令人中文。",
      "高莹",
      "Gao Ying",
      "-",
      "li.ting@lunarbytefusion.example",
      "中国 357723 无锡市 中山路165号",
      "+86 195 3754 7573",
      "东京常常杀位",
      "烟",
    ),
    "zh-Hant" -> List(
      "做夢是誰但別買很喜歡跟孩子人為什麼一條。",
      "楊楓",
      "Yang Feng",
      "-",
      "li.cuifeng@lunarbytefusion.example",
      "台灣 357 竹北市 仁愛路13號",
      "+886 933 495 375",
      "語因現在不用其實",
      "牛奶",
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

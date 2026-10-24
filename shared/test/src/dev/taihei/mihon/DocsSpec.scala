package dev.taihei.mihon

import zio.test.*

import dev.taihei.tsuji.Language

// The seeded values the README and the Scaladoc show. A change to the data changes them: update
// the documentation in the same change.
object DocsSpec extends ZIOSpecDefault:

  private def seeded(tag: String) = Mihon.seeded(1L, Language(tag))

  def spec = suite("DocsSpec")(
    test("the people of the README and the Person Scaladoc") {
      def person(tag: String) = seeded(tag).person
      val ja                  = person("ja")
      assertTrue(
        ja.fullName == "三浦めぐみ",
        ja.latin == "Miura Megumi",
        ja.reading == Some("ミウラ メグミ"),
        person("ru").fullName == "Ольга Жукова",
        person("ru").latin == "Olga Zhukova",
        person("el").fullName == "Γεωργία Παπαδοπούλου",
        person("el").latin == "Georgia Papadopoulou",
        person("ar").fullName == "منى الداود",
        person("ar").latin == "Mona Al Dawod",
        person("he").fullName == "נירית קציר",
        person("he").latin == "Nirit Katzir",
        person("hi").fullName == "प्रतिभा सिंह",
        person("hi").latin == "Pratibha Singh",
        person("zh-Hans").fullName == "姜佩玉",
        person("zh-Hans").latin == "Jiang Peiyu",
        person("ko").fullName == "조혜영",
        person("ko").latin == "Cho Hye-yeong",
      )
    },
    test("the sentence and the addresses of the README and the Address Scaladoc") {
      assertTrue(
        seeded("ru").sentence == "Время перед а знаю быстрее человека права неделю почти перевести.",
        seeded("ja").address.lines == List("日本", "〒873-4446", "京都市中央29-20-14"),
        seeded("hi").address.lines == List("179, मुख्य बाज़ार", "अमृतसर 273444", "पंजाब", "भारत"),
        seeded("en").address.lines == List("7 Lincoln Avenue", "New York City, New York 87344", "United States"),
      )
    },
  )

end DocsSpec

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
        ja.fullName == "田中さちこ",
        ja.latin == "Tanaka Sachiko",
        ja.reading == Some("タナカ サチコ"),
        person("ru").fullName == "Людмила Фомина",
        person("ru").latin == "Liudmila Fomina",
        person("el").fullName == "Βασιλική Κοκολάκη",
        person("el").latin == "Vasiliki Kokolaki",
        person("ar").fullName == "ناديا إبراهيم",
        person("ar").latin == "Nadiyah Ibrahim",
        person("he").fullName == "מירב לנקרי",
        person("he").latin == "Meirav Lankri",
        person("hi").fullName == "विद्या चटर्जी",
        person("hi").latin == "Vidya Chatterjee",
        person("zh-Hans").fullName == "彭薇",
        person("zh-Hans").latin == "Peng Wei",
        person("ko").fullName == "장소희",
        person("ko").latin == "Jang So-hui",
      )
    },
    test("the sentence and the addresses of the README and the Address Scaladoc") {
      assertTrue(
        seeded("ru").sentence == "Люди провёл хотели отец нужна пить знакомы себя со игры.",
        seeded("ja").address.lines == List("日本", "〒873-4446", "京都市中央29-20-14"),
        seeded("hi").address.lines == List("179, मुख्य बाज़ार", "अमृतसर 273444", "पंजाब", "भारत"),
        seeded("en").address.lines == List("7 Lincoln Avenue", "New York City, New York 87344", "United States"),
      )
    },
  )

end DocsSpec

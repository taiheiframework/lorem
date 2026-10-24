package dev.taihei.mihon

import dev.taihei.mihon.data.Form

/**
 * A fake person: a given name and a family name in one language, with the forms a test of an
 * internationalised UI needs. Made by [[Mihon.person]]; not a case class, so that a later minor
 * release can add a field.
 *
 * {{{
 * val ja = Mihon.seeded(1L, Language("ja")).person
 * ja.fullName // "三浦めぐみ": family name first, no space
 * ja.reading  // Some("ミウラ メグミ")
 * ja.latin    // "Miura Megumi"
 * }}}
 */
final class Person private[mihon] (
  givenForm: Form,
  familyForm: Form,
  genderOfName: Gender,
  familyFirst: Boolean,
  separator: String):

  /** The list the given name was drawn from, and so the form of the family name. */
  def gender: Gender = genderOfName

  /** The given name, in the language's script. */
  def givenName: String = givenForm.name

  /**
   * The family name, in the language's script and in the form for [[gender]] where the language
   * inflects family names (Russian, Ukrainian, Bulgarian, Polish, Greek).
   */
  def familyName: String = familyForm.name

  /**
   * The full name in the language's order and with its separator: given name first in most
   * languages, family name first in Japanese, Chinese, Korean, Vietnamese and Hungarian; no space
   * in Japanese, Chinese and Korean.
   */
  def fullName: String = inOrder(givenForm.name, familyForm.name, separator)

  /**
   * The full name in katakana, in name order and separated by a space, where the language writes a
   * reading: Japanese only in 5.0.0, `None` elsewhere.
   */
  def reading: Option[String] =
    for
      g <- givenForm.reading
      f <- familyForm.reading
    yield inOrder(g, f, " ")

  /**
   * The full name romanised, in the language's name order, separated by a space: "Wang Wei",
   * "Ivan Petrov". For a language in Latin script it is [[fullName]], diacritics included.
   */
  def latin: String = inOrder(givenForm.latin, familyForm.latin, " ")

  // The romanised name reduced to ASCII, for e-mail addresses.
  private[mihon] def ascii: String = inOrder(givenForm.ascii, familyForm.ascii, " ")

  private def inOrder(
    g: String,
    f: String,
    sep: String,
  ): String =
    if familyFirst then s"$f$sep$g" else s"$g$sep$f"

  private def members = (gender, givenName, familyName, fullName, reading, latin)

  /** Equal when every member is equal. A field added in a later minor release joins equality. */
  override def equals(other: Any): Boolean = other match
    case that: Person => members == that.members
    case _            => false

  override def hashCode: Int = members.hashCode

  /** The [[fullName]]. For display. Two values with the same toString may still differ, see equals. */
  override def toString: String = fullName

end Person

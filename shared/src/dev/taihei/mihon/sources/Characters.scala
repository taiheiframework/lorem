package dev.taihei.mihon.sources

// One of the word lists Mihon draws from.
private[mihon] object Characters extends SampleWordCollection:
  private val upperCaseLetters = ('A' to 'Z').toArray
  private val lowerCaseLetters = ('a' to 'z').toArray
  private val numbers          = ('0' to '9').toArray
  private val symbols          = "!@#$%^&*()_+-=[]{}|;:,.<>?".toCharArray
  private val chars            = upperCaseLetters ++ lowerCaseLetters ++ numbers ++ symbols

  override lazy val words: List[String] = chars.map(_.toString).toList

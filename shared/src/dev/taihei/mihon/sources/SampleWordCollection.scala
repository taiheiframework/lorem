package dev.taihei.mihon.sources

import java.util.Random

// A list of words of which `apply(random)` returns one, drawn from the caller's generator so that a
// seeded Mihon stays reproducible.
private[mihon] trait SampleWordCollection:
  lazy val words: List[String]

  // An IndexedSeq, so that a draw from a list of a thousand names is not a walk along it.
  private lazy val indexed: IndexedSeq[String] = words.toIndexedSeq

  final def apply(random: Random): String = indexed(random.nextInt(indexed.length))

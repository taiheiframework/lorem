package dev.taihei.mihon.sources

// One of the word lists Mihon draws from.
private[mihon] object FileExtensions extends SampleWordCollection:

  override lazy val words: List[String] = List(
    ".txt",  // Plain text file
    ".pdf",  // Portable Document Format
    ".docx", // Microsoft Word document
    ".xlsx", // Microsoft Excel spreadsheet
    ".pptx", // Microsoft PowerPoint presentation
    ".csv",  // Comma-separated values file
    ".json", // JavaScript Object Notation file
    ".xml",  // Extensible Markup Language file
    ".html", // HyperText Markup Language file
    ".css",  // Cascading Style Sheets file
    ".js",   // JavaScript file
    ".java", // Java source code file
    ".py",   // Python script
    ".rb",   // Ruby script
    ".php",  // PHP script
    ".cpp",  // C++ source code file
    ".c",    // C source code file
    ".go",   // Go source code file
    ".sh",   // Shell script
    ".bat",  // Batch file
    ".exe",  // Windows executable file
    ".dll",  // Dynamic-link library file
    ".iso",  // Disk image file
    ".zip",  // Compressed archive file
    ".rar",  // Compressed RAR archive
    ".tar",  // Unix tarball archive
    ".gz",   // Gzip compressed file
    ".mp3",  // MP3 audio file
    ".wav",  // Waveform audio file
    ".mp4",  // MPEG-4 video file
  )

end FileExtensions

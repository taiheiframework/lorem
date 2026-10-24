package dev.taihei.mihon.sources

// One of the word lists Mihon draws from.
private[mihon] object MimeTypes extends SampleWordCollection:

  override lazy val words: List[String] = List(
    "text/plain",         // Plain text
    "application/pdf",    // PDF document
    "application/msword", // Microsoft Word document
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", // Word (DOCX)
    "application/vnd.ms-excel", // Microsoft Excel spreadsheet
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // Excel (XLSX)
    "application/vnd.ms-powerpoint", // Microsoft PowerPoint presentation
    "application/vnd.openxmlformats-officedocument.presentationml.presentation", // PowerPoint (PPTX)
    "text/csv",                                      // CSV file
    "application/json",                              // JSON data
    "application/xml",                               // XML data
    "text/html",                                     // HTML document
    "text/css",                                      // CSS stylesheet
    "application/javascript",                        // JavaScript file
    "application/java-archive",                      // Java archive (JAR)
    "application/x-python-code",                     // Python bytecode
    "application/x-httpd-php",                       // PHP script
    "text/x-c",                                      // C source code
    "text/x-c++",                                    // C++ source code
    "application/x-sh",                              // Shell script
    "application/x-bat",                             // Batch file
    "application/vnd.microsoft.portable-executable", // Windows executable (EXE)
    "application/x-dosexec",                         // DOS executable
    "application/x-iso9660-image",                   // ISO disk image
    "application/zip",                               // ZIP archive
    "application/x-rar-compressed",                  // RAR archive
    "application/x-tar",                             // TAR archive
    "application/gzip",                              // GZIP compressed file
    "audio/mpeg",                                    // MP3 audio
    "audio/wav",                                     // WAV audio
    "video/mp4",                                     // MP4 video
  )

end MimeTypes

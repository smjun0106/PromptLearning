
### Reference
```
https://github.com/ad-freiburg/pdfact
```

### Execution 
```
java -jar pdfact.jar --format json input.pdf output.txt
```

### Extracted Items
```
figure,  other,  appendix,  keywords,  heading, page-header, footer, acknowledgments,  caption,  toc,  abstract, footnote, body,
itemize-item,  title,  reference,   affiliation,   general-terms,  formula,
categories, table, authors
```

### Pdfact Command
```

java -jar pdfact.jar --help
usage: pdfact [-h] [--format <format>] [--units <units>] [--include-roles <roles>]
              [--exclude-roles <roles>] [--visualize <path>] [--with-control-characters]
              [--debug-pdf-parsing] [--debug-character-extraction] [--debug-splitting-ligatures]
              [--debug-merging-diacritics] [--debug-text-line-detection] [--debug-word-detection]
              [--debug-text-block-detection] [--debug-semantic-role-detection]
              [--debug-paragraph-detection] [--debug-word-dehyphenation] [--pdfjs-mode] <pdf-file>
              [<output-file>]

A tool to extract the text, structure and layout from PDF files.

positional arguments:
  <pdf-file>             The path to the PDF file to be processed.
  <output-file>          The path to the file to which the extraction output should be written.
                         If not specified, the output will be written to stdout.

named arguments:
  -h, --help             show this help message and exit
  --format <format>      The output format.
                         - Available options: txt, xml, json.
                         - Default: "txt".
                         In case of txt, the text elements  will  be extracted as plain text, in the
                         format: one text element  per  line.  In  case  of  xml  or  json, the text
                         elements will be extracted  together  with  their layout information, e.g.,
                         their positions in the PDF file, their fonts and their colors.
  --units <units>        The granularity in which the  elements  should  be extracted in the output,
                         separated by ",".
                         - Available options:  characters,  pages,  figures,  blocks, shapes, words,
                         areas, paragraphs, lines.
                         - Default: "paragraphs".
                         For example, when the script  is  called  with  the option "--units words",
                         the output will be broken  down  by  words,  that  is:  the text and layout
                         information are provided word-wise.
  --include-roles <roles>
                         The list of the semantic roles to include, separated by ",".
                         - Available options:  figure,  other,  appendix,  keywords,  heading, page-
                         header, footer, acknowledgments,  caption,  toc,  abstract, footnote, body,
                         itemize-item,  title,  reference,   affiliation,   general-terms,  formula,
                         categories, table, authors.
                         -   Default:    "figure,other,appendix,keywords,heading,page-header,footer,
                         acknowledgments,caption,toc,abstract,footnote,body,itemize-item,title,
                         reference,affiliation,general-terms,formula,categories,table,authors".
                         Only the elements with a semantic role  that  is included in this list will
                         be extracted. All other elements  won't  be  extracted. For example, if the
                         script is  called  with  the  option  "--include-roles  headings,body", the
                         output will only contain  the  text  elements  (and  optionally, the layout
                         information) belonging to a heading or  a body text paragraph. Per default,
                         all available semantic roles are  included,  that  is: all elements will be
                         extracted, regardless of the semantic roles.
                         NOTE: The detection of the semantic roles  of the text elements is still in
                         an experimental state. So  don't  expect  the  semantic  roles to be highly
                         accurate.
  --exclude-roles <roles>
                         The list of the semantic roles to exclude, separated by ",".
                         - Available options:  figure,  other,  appendix,  keywords,  heading, page-
                         header, footer, acknowledgments,  caption,  toc,  abstract, footnote, body,
                         itemize-item,  title,  reference,   affiliation,   general-terms,  formula,
                         categories, table, authors.
                         - Default: "".
                         All elements with a semantic role  that  is  included in this list won't be
                         extracted. For example, if the script is called with the option "--exclude-
                         roles body", the  text  (and  layout  information)  belonging  to body text
                         paragraphs won't be extracted. Per  default,  no semantic role is excluded,
                         that is: all elements will be extracted.
                         NOTE: The detection of the semantic roles  of the text elements is still in
                         an experimental state. So  don't  expect  the  semantic  roles to be highly
                         accurate.
  --visualize <path>     The path to a  file  (ending  in  *.pdf)  to  which  a visualization of the
                         extracted elements (that is: the original  PDF file enriched which bounding
                         boxes around the extracted  elements  and  the  semantic  roles in case the
                         unit is "paragraph") should be  written  to.  The  file  doesn't have to be
                         existent before. If not specified, no such visualization will be created.
  --with-control-characters
                         Add the following control characters to the TXT serialization output:
                         - "^L" ("form feed") between two elements  when a page break occurs between
                         the two elements in the PDF.
                         - "^A" ("start of heading") in front of headings.
  --debug-pdf-parsing    Print debug info about the PDF parsing step.
  --debug-character-extraction
                         Print debug info about the character extraction step.
  --debug-splitting-ligatures
                         Print debug info about the splitting ligatures step.
  --debug-merging-diacritics
                         Print debug info about the merging diacritics step.
  --debug-text-line-detection
                         Print debug info about the text line detection step.
  --debug-word-detection
                         Print debug info about the word detection step.
  --debug-text-block-detection
                         Print debug info about the text block detection step.
  --debug-semantic-role-detection
                         Print debug info about the semantic roles detection step.
  --debug-paragraph-detection
                         Print debug info about the paragraphs detection step.
  --debug-word-dehyphenation
                         Print debug info about the word dehyphenation step.
  --pdfjs-mode           Enables the pdf.js mode, that is: a mode  that outputs the text in a format
                         as required by the tool from  Robin  that improves the search functionality
                         of pdf.js





```

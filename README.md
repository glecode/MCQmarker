# MCQmarker
MCQmarker marks and aggregates multiple choice answers across different examinations, provided that the individual answer sheets are in a csv format.  It is run in a parent directory containing the directories of student answer sheets.

MCQmarker is a kind of 'hope we don't have to use' backup for when normal systems are not working, or for when transfering MCQ exam paper questions to an alternative online format seems too costly/risky.  Instead, students can read their questions in a familiar format, but complete their answers in csv, see e.g. the versions of <i>student1.csv</i> in ABC101 and ABC102.

INSTRUCTIONS
1. Aside from the question numbering style, the format must be as in student1.csv, though the answer sheet filenames can be anything provided there is a csv extension.  Students mark answers with X or x.
2. A mark scheme document called <i>markscheme.csv</i> needs to be put in each directory of answer sheets.  Only directories containing a mark scheme will be processed.
3. Run MCQmarker in the parent directory containing the directories of answer sheets for each examination.

OUTPUTS
1. A spreadsheet of marks (<i>Student ID, Name, Mark</i>) in each directory in the format <i>DirectoryName_MCQ_marks.csv</i>.
2. A file <i>no_csv_extension.csv</i> in each directory, containing a log of files it found without a csv extension and therefore did not process.
3. A file <i>csv_but_not_a_record.csv</i> in each directory, containing a log of files it found that were in csv format but did not seem to be answer sheet files (the script checks whether the top left hand corner element is "Student ID:").

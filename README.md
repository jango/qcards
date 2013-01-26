qcards
======

This makes preparation of [language] flash cards easy. In principle,
the workflow is something like that:

1. Take a list of words and put them into a CSV file. The only formatting
you are allowed to use is:
    * `*` in front of a letter will make it bold in the final format;
    * `$` in front of a letter will make it italicized in the final format;
    * `_` in front of a letter will make it underlined in the final format;

*Note*: you may escape existing `*, $, _` by putting `\` in front of it; you can
ecape `\` by `\\`. All other characters will be taken as is. Unicode is used
when reading/writing files.

2. Write a configuration file for qcards, like the one that appears here:
    https://github.com/jango/macedonian-qcards/blob/master/macedonian.cfg

This configuration file tells `qcards` how to parse your CSV and where to
output the result files (note that in order to generate PDF files, you
need to have LaTeX installed).

*Note*: you can have multiple [latex] and [csv] sections in the configuration
file.

3. Run `qcards -c /path/to/config.cfg` to generate beautiful output.

4. Start studying using PDF cards, or, import CSVs into your favourite
flash card app.

If you want to see example of the cards generated by the app, see:
   https://github.com/jango/macedonian-qcards/tree/master/output

The project is licensed under GPL, please share.

Happy learning! (:

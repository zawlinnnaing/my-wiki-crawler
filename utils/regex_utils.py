import re

# regex for splitter large text into lists of words
# SPLITTER_RE = r'[$/:?{~}!"^ _`()\[\]]'
SPLITTER_RE = r'။'

# regex for any non-burmese characters
NON_MM_RE = r'[a-zA-Z0-9\/:&?.%\n "=↑,]+'

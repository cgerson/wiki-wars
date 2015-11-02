# wiki-wars

This script has two options:
- Common links: generate a list of the Wikipedia links that selected pages have in common, or
- Common words: return number of words pages have in common

How to use:

Let's say we want to look at pages 'Spain' and 'Existentialism'.

1) Common links

Running on the CL: python wiki_wars.py Spain Existentialism

Returns:

These pages have the following links in common: 
/wiki/Averroes
/wiki/Integrated_Authority_File
/wiki/Humanism
/wiki/DMOZ
/wiki/Don_Quixote
/wiki/International_Standard_Book_Number
/wiki/Modernism
/wiki/National_Diet_Library
/wiki/Europe
/wiki/Maimonides

2) Common words

Running on the CL: python wiki_wars.py Spain Existentialism --words

Returns:

These pages have 647 words in common.

*** project in progress ***
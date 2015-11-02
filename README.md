# wiki-wars

This script has two options:
- Common links: generate a list of the Wikipedia links that will lead from one page to another
- Common words: return number of words pages have in common

How to use:

Let's say we want to look at pages 'Spain' and 'Existentialism'.

1) Common links

Running on the CL: python wiki_wars.py Spain Existentialism

Returns:

These links will lead you directly from Spain to Existentialism  
Humanism  
Averroes  
Modernism  
Maimonides  

2) Common words

Running on the CL: python wiki_wars.py Spain Existentialism --words

Returns:

These pages have 647 words in common.

*** project in progress ***
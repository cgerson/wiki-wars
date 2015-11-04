''' Measure the correlation between number of words and number of links.

Estimate runtime of returning links of a page.

'''

from wiki_wars import pageObject
import sys


def links_and_words_print(keyword):

    page_object = pageObject(keyword)

    set_links = set(page_object.return_links())
    list_words = page_object.return_filtered_words()

    print keyword+ " Links: {0}".format(len(set_links))
    print keyword+ " Words: {0}".format(len(list_words))
    print
    
    return set_links

    
def main(keyword):

    set_links = links_and_words_print(keyword)

    for meta_keyword in set_links:

        meta_set_links = links_and_words_print(meta_keyword)

        for meta_meta_keyword in meta_set_links:
            
            links_and_words_print(meta_meta_keyword)

            
if __name__ == "__main__":

    main(sys.argv[1])

''' 
Print number of links and number of words of articles 
that are linked to within a selected page.

'''

from wiki_wars import pageObject
import sys
import time


def links_and_words_print(keyword):

    page_object = pageObject(keyword)

    t = time.time()
    set_links = set(page_object.return_links()) #collect links
    print keyword+ "Runtime (links): {0}".format(t-time.time())
    
    list_words = page_object.return_filtered_words() #collect words

    #print number of links and number of words
    print keyword+ " Links: {0}".format(len(set_links))
    print keyword+ " Words: {0}".format(len(list_words))
    print
    
    return set_links #return to traverse through

    
def main(keyword):

    set_links = links_and_words_print(keyword)

    for meta_keyword in set_links:

        meta_set_links = links_and_words_print(meta_keyword)

            
if __name__ == "__main__":

    main(sys.argv[1])

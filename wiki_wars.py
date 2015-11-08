from bs4 import BeautifulSoup
import requests
import re
import sys

from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
stops = set(stopwords.words("english"))
import string

import time


class pageObject:
    
    def __init__(self,keyword):
        self.keyword = keyword
    
    def return_soup(self):
        """ Return BeautifulSoup object of given Wikipedia page """
        
        url = 'https://en.wikipedia.org/wiki/' + self.keyword
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page,"html.parser")
        return soup

    def return_links(self):
        """ Return (unique) links to other Wikipedia articles included in given Wikipedia page """
        
        soup = self.return_soup()

        links = []
        for line in soup.find_all('a',attrs={'href':re.compile('wiki(?!pedia)')}):
            links.append(line['href'][6:]) #cut off "/wiki/

        return set(self.filter_links(links))

    def filter_links(self,links_list):
        """ Filter links to exclude links appearing in every page """
        
        #consider allowing for "Special:Random" link
        good_links = []
        for link in links_list:
            bad = [self.keyword,"Talk","Category","Help","Wikipedia","File",
                   "Main_Page","Portal","Special","Template",".org"]
            bools = [link.find(x) == -1 for x in bad]
            if False not in bools:
                good_links.append(link)

        return good_links
    
    def return_filtered_words(self):
        """ Parse body of document  and return list of stemmed words, 
        excl. stopwords, punctuation and numbers """
        
        soup = self.return_soup()

        bag_of_words = []
        for line in soup.findAll('p'):
            if line.text:
                bag_of_words.extend(line.text.strip().split())
        bow = " ".join(bag_of_words)

        text_nonums = re.sub("\d+", " ", bow) #no numbers
        text_nopunct = re.sub(r'[^\w\s]','',text_nonums) #no punctuation

        words = wordpunct_tokenize(text_nopunct.lower()) #could use other tokenizer since no punct left

        unstemmed = filter(lambda token: token not in stops \
                      and len(token)>1, words)
        
        stemmed = [porter_stemmer.stem(w) for w in unstemmed]

        return stemmed

        
def return_direct_links(start_page,end_page):
    """ Parse through common links of start_page and end_page to find 
    whether end_page can be found within links of any common links.
    
    Possibility still exists that there is one page through which
    one could connect start_page and end_page. This function only tries 
    to reduce possibilities."""
    
    page_object_start = pageObject(start_page)
    page_object_end = pageObject(end_page)

    #set of links common to both start and end page
    common_links = page_object_start.return_links() & page_object_end.return_links()

    direct_links = []
    for link in common_links:
        page_object = pageObject(link)
        if end_page in page_object.return_links():
            direct_links.append(link)

    return direct_links

    
def main(pages,words):
    """Two options: words or war.

    If words chosen, script returns number of words in common between two pages.

    If war chosen (default), script returns any articles that will lead directly from 
    start_page to end_page (chosen from within links common to both pages, 
    to reduce computation time)."""
    
    print "="*80
    print "Finding a connection..."

    d = {}

    if words: #if words option chosen, print number of words in common (excl. stopwords)

        for i,k in enumerate(pages):
            page_object = pageObject(k)
            d[i] = set(page_object.return_filtered_words())

        common_words = reduce(lambda x,y: x&y, d.values())
        
        print "These pages have {0} words in common.".format(len(common_words))
            
    else: #otherwise, print all links that will lead directly from starting page to ending page

        print "-"*80

        direct_links = return_direct_links(pages[0],pages[1]) #only passes first two page arguments
        
        if len(direct_links)>0: #check if there are any links that lead directly from start_page to end_age
            print "These links will lead you directly from {0} to {1}".format(pages[0],pages[1])
            for link in direct_links:
                print link
        else:
            print "No link found that will lead from {0} to {1}".format(pages[0],pages[1])
                     
        print "-"*80

    
if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Find connections between Wikipedia pages, \
either by common links or common words.')

    #add argument options
    parser.add_argument('pages', nargs='*',
                        help='the Wikipedia pages to be parsed')
    parser.add_argument('--words', action='store_const', const='words',
                        help='return the number of words in common')

    args = parser.parse_args()

    t = time.time()
    
    main(args.pages,args.words)

    print "Runtime: {0} seconds.\n".format(time.time() - t)

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

class keywordObject:
    
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
        """ Return links to other Wikipedia articles included in given Wikipedia page """
        
        links = []
        soup = self.return_soup()
        for line in soup.find_all('a',attrs={'href':re.compile('wiki(?!pedia)')}):
            links.append(line['href'])
        links_filtered = self.filter_links(links)
        return links_filtered

    def filter_links(self,links_list):
        """ Filter links to exclude links appearing in every page """
        
        #consider allowing for "Special:Random" link
        good_links = []
        for link in links_list:
            bad = ["wiki/Category","wiki/Help","wiki/Wikipedia","wiki/File",
                   "wiki/Main_Page","wiki/Portal","wiki/Special",
                   ".org"]
            bools = [link.find(x) == -1 for x in bad]
            if False not in bools:
                good_links.append(link)
        return good_links
    
    def return_filtered_words(self):
        """ Parse document and return list of stemmed words, 
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
        stemmed = []
        for w in unstemmed:
            stemmed.append(porter_stemmer.stem(w))
        return stemmed

    
def main(pages,words):

    print "="*80
    print "Finding a connection..."

    d = {}

    if words: #if words option chosen, print number of words in common (excl. stopwords)

        for i,k in enumerate(pages):
            keyword_object = keywordObject(k)
            d[i] = set(keyword_object.return_filtered_words())
        common_words = reduce(lambda x,y: x&y, d.values())
        
        print "These pages have {0} words in common.".format(len(common_words))
            
    else: #if words not chosen, print Wikipedia article links that selected pages share

        for i,k in enumerate(pages):
            keyword_object = keywordObject(k)
            d[i] = set(keyword_object.return_links())
        common_links = reduce(lambda x,y: x&y, d.values())
        
        print "These pages have the following links in common: "
        for link in common_links:
            print link

    
if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Find similarities between Wikipedia pages, either by common links or common words.')

    #add argument options
    parser.add_argument('pages', nargs='*',
                        help='the Wikipedia pages to be parsed')
    parser.add_argument('--words', action='store_const', const='words',
                        help='return the number of words in common')

    args = parser.parse_args()
    
    main(args.pages,args.words)

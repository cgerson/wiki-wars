from bs4 import BeautifulSoup
import requests
import re
import sys

class keywordToLinks:
    
    def __init__(self,keyword):
        self.keyword = keyword
    
    def return_soup(self):
        url = 'https://en.wikipedia.org/wiki/' + self.keyword
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page,"html.parser")
        return soup

    def return_links(self):
        links = []
        soup = self.return_soup()
        for line in soup.find_all('a',attrs={'href':re.compile('wiki(?!pedia)')}):
            links.append(line['href'])
        links_filtered = self.filter_links(links)
        return links_filtered

    def filter_links(self,links_list):
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

def main():
    d = {}
    for i,k in enumerate(sys.argv[1:]):
        keyword_object = keywordToLinks(k)
        d[i] = set(keyword_object.return_links())
    common_links = reduce(lambda x,y: x&y, d.values())
    for link in common_links:
        print link
    
if __name__ == "__main__":
    main()
import requests
import re
import lxml.html
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
import timeit

def extractLinkRegEx(txt):
    tgs = re.compile(r'<a[^<>]+?href=([\'\"])(.*?)\1', re.IGNORECASE)
    return [match[1] for match in tgs.findall(txt)]

def extractLinksLxml(txt):
    lst = []
    dom = lxml.html.fromstring(txt)
    for l in dom.xpath('//a/@href'):
        lst.append(l)
    return lst        


def extractLinksHtmlParser(txt):
    lst = []
    dom = HTMLParser(txt)
    for tag in dom.tags('a'):
        attrs = tag.attributes
        if 'href' in attrs:
            lst.append(attrs['href'])
        return lst   

def extractBs(txt):
    lst = []
    s = BeautifulSoup(txt, 'lxml')
    for tag in s.find_all('a', href=True):
        lst.append(tag['href'])
    return lst    


def printList(lst):
    for l in lst:
        print('Level 1 -> ' + l) 

def printListWithFltr(lst, fltr):
    for l in lst:
        if inFilter(l, fltr):
            print('Level 1 -> ' + l)

def inFilter(l, fltr):
    r = False
    for f in fltr:
        if f in l:
            r = True 
            break
    return r   

def followList(lst, fltr, prt=False):
    for l in lst:
        if inFilter(l, fltr):
            print('Level 1 -> ' + l)
            if prt == False:
                r = requests.get(l)
                res = extractBs(r.text)
                for r in res:
                    print('Level 2 -> ' + r)                

tcode = '''
def extractBs(txt):
    lst = []
    s = BeautifulSoup(txt, 'lxml')
    for tag in s.find_all('a', href=True):
        lst.append(tag['href'])
    return lst 
    '''


r = requests.get('https://edfreitas.me')
#print(extractLinkRegEx(r.text))
#printList(extractLinkRegEx(r.text))
#printList(extractLinksLxml(r.text)) 
#printList(extractLinksHtmlParser(r.text))
printList(extractBs(r.text))

tsetup = "from bs4 import BeautifulSoup"
print(timeit.timeit(setup = tsetup,
                    stmt = tcode,
                    number= 10000))

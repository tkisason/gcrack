#!/usr/bin/python

def scrape_links_and_wordlistify(links,lower=False,verbose=1):
    import nltk
    import requests
    import string
    raw = ''
    wordlist = []
    for site in links:
        try:
            if verbose == 1:
                print '[+] fetching data from: ',site
            raw = requests.get(site).content
            if lower != False:
                wordlist += list(set(nltk.clean_html(raw).split()))
            else:
                wordlist += map(lambda x: string.lower(x),list(set(nltk.clean_html(raw).split())))
        except:
            if verbose == 1:
                print '[-] Skipping url: ',site
    return wordlist 


def google_wordlist(queries, results_per_query=10, lower=False, verbose=1):
    from google import search
    links = []
    num = 0
    for q in queries:
        try:
            for link in search(q,stop=results_per_query):
                if num >= results_per_query:
                    break
                links.append(link)
                num += 1
        except:
            if verbose == 1:
                print '[-] google fails'
    return scrape_links_and_wordlistify(links,lower)


if __name__ == '__main__':
    __program__ = 'mkwordlist'
    __url__ = 'https://github.com/tkisason/gcrack'
    __author__ = 'Tonimir Kisasondi <kisasondi@gmail.com>'
    __copyright__ = 'Copyright (c) 2012'
    __license__ = 'GPLv3'
    __version__ = '0.5'
    import argparse
    desc = 'Generate custom wordlists based on google queries and screen scrapes of N top links returned by google queries for each keyword'
    print '\n'+__program__+' '+__version__+' by '+__author__+'\n'+__copyright__+' Distributed under '+ __license__+''
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('KEYWORDS_FILE', help='Load keywords from KEYWORDS_FILE, one line == one search query')
    parser.add_argument('OUTPUT_FILE', help='Your wordlist will be saved/appended to OUTPUT_FILE')
    parser.add_argument('-l','--lowercase', help='Make sure all capitals are LOWERCASE, useful if you will use rules to mutate your wordlist',action='store_true')
    parser.add_argument('-n','--number', help='Use NUMBER of top google links for scraping instead of default 5 ',type=int, default=10)
    args=parser.parse_args()
    keywords = open(args.KEYWORDS_FILE,'r').read().strip().split("\n")
    print '[+] Googling for keywords'
    owl = google_wordlist(keywords,int(args.number),args.lowercase)
    print '[+] Removing duplicate entries from wordlist'
    owl = list(set(owl))
    wl = open(args.OUTPUT_FILE,'a+')
    print '[+] Writing wordlist to :',args.OUTPUT_FILE
    for line in owl:
        wl.write(line+'\n')
        wl.flush()
    wl.close()
    print '[+] Done!'

#!/usr/bin/env python

import hashlib
import urllib2
import random,time
import lxml.html
from urlparse import urlparse,urljoin

try:
    import nltk
except:
    nltk = 0

__program__ = 'gcrack'
__url__ = 'https://github.com/tkisason/gcrack'
__author__ = 'Tonimir Kisasondi <kisasondi@gmail.com>'
__copyright__ = 'Copyright (c) 2012'
__license__ = 'GPLv3'
__version__ = '1.5'

useragent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0C)'

def get_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', useragent)]
    usock = opener.open(url)
    data = usock.read()
    usock.close()
    return data

def parser(data,url,type="a",stype="href"):
    if url.find('http://') == -1:
        url = 'http://'+url
    content = lxml.html.fromstring(data)
    links = []
    for link in content.cssselect(type):
        links.append(urljoin(url,link.get(stype)))
    return links

def diff_netloc(crawlurl,data):                                
    urllist = parser(data,crawlurl)
    if crawlurl.find('http://') == -1:
        crawlurl = 'http://'+crawlurl
    outlist = []
    ourl = urlparse(crawlurl).netloc
    urllist = filter(lambda x: x.find("google")==-1 and x.find("youtube") == -1 and x.find("blogger") == -1,urllist)
    for url in urllist:
        if urlparse(url).netloc != ourl:
            if url.find("google.") == -1:
                outlist.append(url.replace("https://","http://")) #1337 downgrade attack ;)
    return outlist

def hash(data):
    hashes = []
    for h in hashlib.algorithms:
        hashes.append(h+':'+hashlib.new(h,data).hexdigest())
    try:
        hashes.append('ntlm:'+hashlib.new('md4', data.encode('utf-16le','ignore')).hexdigest()) # NTLM
    except UnicodeDecodeError:
	pass # ignore errors with decoding unicodes
        # print "NTLM hash failed: "+data
    return hashes

def get_bag_of_words(query):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = "http://www.google.com/search?hl=en&safe=off&q="+query
    headers={'User-Agent':user_agent,} 
    request=urllib2.Request(url,None,headers)
    response = urllib2.urlopen(request)
    time.sleep(random.random())
    data = response.read()
    links = diff_netloc(url,data)
    for l in links[:3]:
        try:
            data += "\n" + get_url(l) + "\n"
        except:
            pass
    if nltk:
        data = nltk.clean_html(data)
    data = list(set(data.split()))
    final = []
    for el in data:
        final += el.split(":")
    return final

def rfile(runfile, option,input=''):
    if option == "read":    # random r/w
        F = open(runfile, "a+") #a+ creates file if it doesn't exist, skips try/except
        F.seek(0)
        data = F.read()
        F.close()               #If someone knows a better way to do this, let me know
        return data
    if option == "append":
        F = open(runfile,"a")
        F.write(input)
        F.close()
        return 1

def google_attack(passlist,verbose=1):
    hashlist = list(passlist)
    wordlist = []
    cracks = []
    skip = 0
    skipped_hashes = 0
    runfile = argv[1]+".run"
    for pwd in hashlist:
        rf = rfile(runfile,"read")
        if rf.find(pwd) >= 0:
            hashlist = filter(lambda x: x!= pwd,hashlist)
            skipped_hashes += 1
            if verbose==1:
                print "[-] Removing already cracked hash: "+pwd
    for pwd in hashlist:
        wordlist = get_bag_of_words(pwd)
        skip = 0
        for word in wordlist:
            if skip == 1:
                break
            hashes = hash(word)
            for h in hashes:
                h = h.split(":")
                if h[1] == pwd:
                    rfile(runfile,"append",str(h[0]+"("+word+")\t\t"+h[1]+"\n"))
                    cracks.append(h[0]+"("+word+")\t\t"+h[1])
                    if verbose == 1:
                        print h[0]+"("+word+")\t\t"+h[1]
                    skip = 1
        if skip == 0:
            rfile(runfile,"append",str("??????????\t\t"+pwd+"\n"))
    return cracks,skipped_hashes


if __name__ == "__main__":
    from sys import argv
    if len(argv) != 2:
        print "usage: ",argv[0]," [file_with_hashes]"
        print "gcrack will automatically try and create [file_with_hashes].run for hashes that have been tryed/cracked"
        print __program__," " ,__version__, "by", __author__," ",__copyright__," Distributed under ", __license__
    else:
        filehashes = open(argv[1]).read().strip().split()
        print "[+] Hashes loaded, using google_attack to crack them"
        cracks = google_attack(filehashes)
        skipped_hashes = cracks[1]
        cracks= cracks[0]
        print "\n[+] Found ",str(len(cracks)+skipped_hashes)," of ", str(len(filehashes))




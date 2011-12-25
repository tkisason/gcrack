#!/usr/bin/env python

import hashlib
import urllib2
import random,time

try:                # pip install nltk
    import nltk
except:
    nltk=0


__program__ = 'gcrack'
__url__ = 'https://github.com/tkisason/gcrack'
__author__ = 'Tonimir Kisasondi <kisasondi@gmail.com>'
__copyright__ = 'Copyright (c) 2011'
__license__ = 'GPLv3'
__version__ = '1.0'

def hash(data):
    hashes = []
    for h in hashlib.algorithms:
        hashes.append(h+':'+hashlib.new(h,data).hexdigest())
    return hashes

def get_bag_of_words(query):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = "http://www.google.com/search?hl=en&safe=off&q="+query
    headers={'User-Agent':user_agent,} 
    request=urllib2.Request(url,None,headers)
    response = urllib2.urlopen(request)
    time.sleep(random.random())
    data = response.read()
    if nltk:
        data = nltk.clean_html(data)
    data = list(set(data.split()))
    final = []
    for el in data:
        final += el.split(":")
    return final

def google_attack(passlist):
    wordlist = []
    cracks = []
    skip = 0
    for p in passlist:
        wordlist += get_bag_of_words(p)
    for pwd in passlist:
        skip = 0
        for word in wordlist:
            if skip == 1:
                break
            hashes = hash(word)
            for h in hashes:
                h = h.split(":")
                if h[1] == pwd:
                    cracks.append(h[0]+"("+word+")\t\t"+h[1])
                    skip = 1
    return cracks


if __name__ == "__main__":
    from sys import argv
    if len(argv) != 2:
        print "usage: ",argv[0]," [file_with_hashes]"
        print __program__," " ,__version__, "by", __author__," ",__copyright__," Distributed under ", __license__
    else:
        filehashes = open(argv[1]).read().strip().split()
        print "[+] Hashes loaded, using google_attack to crack them"
        cracks = google_attack(filehashes)
        for elem in cracks:
            print elem
        print "[+] Found ",str(len(cracks))," of ", str(len(filehashes))



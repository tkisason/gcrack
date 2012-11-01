#!/usr/bin/env python

import hashlib
import mkwordlist #depends on python-google, python-requests, python-nltk

def hash(data):
    hashes = []
    for h in hashlib.algorithms:
        hashes.append(h+':'+hashlib.new(h,data).hexdigest())
    try:
        hashes.append('ntlm:'+hashlib.new('md4', data.encode('utf-16le','ignore')).hexdigest()) # NTLM
    except UnicodeDecodeError:
	pass # ignore errors with decoding unicodes
        # print 'NTLM hash failed: '+data
    return hashes

def rfile(runfile, option,input=''):
    if option == 'read':    # random r/w
        F = open(runfile, 'a+') #a+ creates file if it doesn't exist, skips try/except
        F.seek(0)
        data = F.read()
        F.close()               #If someone knows a better way to do this, let me know
        return data
    if option == 'append':
        F = open(runfile,'a')
        F.write(input)
        F.close()
        return 1

def old_mutate(wordlist, verbose=1): # simple mutators, you can add yours here...
    if verbose == 1:
        print '[+] Adding extra splits... '
    output = wordlist
    splits = [':',' ','"','\r']
    for sp in splits:
        output += sum(( map(lambda x:x.split(sp),wordlist) ),[])
    print '[+] Deduplicating list'
    output = list(set(output))
    return output

def mutate(wordlist, verbose=1): # simple mutators, you can add yours here...
    if verbose == 1:
        print '[+] Adding extra splits... '
    output = []
    splits = [':']
    for line in wordlist:
        for sp in splits:
            output += line.split(sp)
    if verbose == 1:
        print '[+] Deduplicating list'
    output = list(set(output))
    return output

def google_attack(passlist,runfile,rpq,verbose=1):
    hashlist = list(passlist)
    wordlist = []
    cracks = []
    skip = 0
    skipped_hashes = 0
    for pwd in hashlist:
        rf = rfile(runfile,'read')
        if rf.find(pwd) >= 0:
            hashlist = filter(lambda x: x!= pwd,hashlist)
            skipped_hashes += 1
            if verbose==1:
                print '[-] Removing already cracked hash: '+pwd
    wordlist = mkwordlist.google_wordlist(hashlist, results_per_query=rpq, lower=False, verbose=1)
    wordlist = mutate(wordlist)
    if verbose == 1:
        print '[+] Cracking...'
    for pwd in hashlist:
        skip = 0
        for word in wordlist:
            if skip == 1:
                break
            hashes = hash(word)
            for h in hashes:
                h = h.split(':')
                if h[1] == pwd:
                    rfile(runfile,'append',str(h[0]+'('+word+')\t\t'+h[1]+'\n'))
                    cracks.append(h[0]+'('+word+')\t\t'+h[1])
                    print h[0]+'('+word+')\t\t'+h[1]
                    skip = 1
        if skip == 0:
            rfile(runfile,'append',str('??????????\t\t'+pwd+'\n'))
    return cracks,skipped_hashes

if __name__ == '__main__':
    __program__ = 'gcrack'
    __url__ = 'https://github.com/tkisason/gcrack'
    __author__ = 'Tonimir Kisasondi <kisasondi@gmail.com>'
    __copyright__ = 'Copyright (c) 2012'
    __license__ = 'GPLv3'
    __version__ = '2.0'
    import argparse
    desc = 'Generate custom wordlists based on google queries and screen scrapes of N top links returned by google queries for each keyword'
    print '\n'+__program__+' '+__version__+' by '+__author__+'\n'+__copyright__+' Distributed under '+ __license__+''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n','--number', help='Use NUMBER of top google links for scraping instead of default 3',type=int, default=3)
    parser.add_argument('INPUT_FILE', help='File with hashes to crack, gcrack will automatically try and create INPUT_FILE.run with hashes that have been tryed/cracked')
    args=parser.parse_args()
    filehashes = open(args.INPUT_FILE).read().strip().split()
    print '[+] Hashes loaded, using google_attack to crack them'
    print '[+] Using top ',str(args.number) + ' links to attempt crack'
    cracks = google_attack(filehashes,runfile=str(args.INPUT_FILE+'.run'),rpq=args.number)
    skipped_hashes = cracks[1]
    cracks= cracks[0]
    print '\n[+] Found ',str(len(cracks)+skipped_hashes),' of ', str(len(filehashes))
    print '[+] Check file: ', str(args.INPUT_FILE+'.run') , ' for complete list of cracked hashes'

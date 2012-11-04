# gcrack 2.1
by Tonimir Kisasondi <tonimir.kisasondi@foi.hr>
Faculty of Organization and Informatics
Open Systems and Security Lab
Copyright (c) 2011-2012  Released under GPLv3

###Contributors:
Tonimir Kišasondi - (https://github.com/tkisason)
Vlatko Košturjak - Kost (https://github.com/kost)

###Thanks to:
Mario Vilas and his python-google lib (https://github.com/MarioVilas/google)

###Depends on:
python-nltk, python-google, python-beautifulsoup, python-requests
hint: use pip to install dependancies like:
		# pip install nltk google requests BeautifulSoup

###What's the gcrack suite:

gcrack is a set of scripts that helps you crack passwords with google's search. It is composed of the following scripts:

	gcrack.py - crack a set of arbitrary hashes with the help of google's search of those hashes.
	
	gwordlist.py - generate a wordlist based on the the input keywords file
	(generates raw or lowercased wordlist that is great for mutation)
	(this tool was previously named mkwordlist)

All scripts have helpfiles with -h option, so use the -h flag, but all tools are too simple...


gcrack.py cracks and identifies arbitrary hashes (md5, sha1, sha224, sha256, sha384, sha512 and ntlm) by googling for the hash and use top 3 (or any number you specify) pages as a wordlist. If your hash was leaked and cracked, it will be cracked or you will be notified that a resultant hash was detected in google results (useful if you want to see if a hash was compromised). The input file can contain any kind of hash you want, if the plaintext is found in the google results, you will be notified what kind of hash that is. 

gcrack.py generates [filewithhashes].run file that is a resume/report for all hashes that have been tested or found, if your session breaks, or cracking fails, hashes that have not been found will have ??????????\t\t[hash] format in the run file. Simply remove the unknown hashes in the runfile and rerun the script and it will resume cracking.

**REMEMBER! gcrack.py will send all the hashes to google's search via a plaintext protocol. If you are concenrned and you don't want to send those hashes to google, don't use gcrack! It's better to use gwordlist.py to generate a customized wordlist based on some keywords and use a offline password cracker like john or hashcat.**

You can use the testhashes file to test the gcrack.py, it should find all 8 hashes. Gcrack knows to be a bit slow, but it's the same cost to crack about 8 or 80 hashes, so be patient. :)

###Future improvements/TODO:
* This is just a sliver of something far far bigger that's going to be released soon...
* E-mail me ;) 

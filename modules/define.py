import urllib2
import HTMLParser
import re
import sys

def printable(text):
	return re.sub('[\x00-\x1f]','',text)

def cleanHTML(html):
	return printable(re.sub(' +',' ',re.sub(r'<[^>]*>','',html))).strip(' ')

def gethttp(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.1')]
		return ''.join(opener.open(url))
	except Exception as e:
		print 'EXCEPTION WITH URL "'+url+'"'
		print e
		return ''

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Python script')]
word = sys.argv[1]
site = ''.join(opener.open('http://dictionary.reference.com/browse/'+urllib2.quote(word)))

if site.find('<span class="nr">') == -1:
	if site.find('<div class="pbk">') == -1:
		print 'ignoring'
	else:
		exp = site.split('<div class="pbk">')[1]
		if exp.find('<div class="dndata">') != -1:
			exp = exp.split('<div class="dndata">')[1]
		elif exp.find('<div class="luna-Ent">') != -1:
			exp = exp.split('<div class="luna-Ent">')[1]
		else:
			print 'ERROR (could not find definition)'
			exit()
		exp = exp[:exp.find('</div>')]
		print word+' - '+cleanHTML(exp)
else:
	site = site[site.find('<span class="nr">')+17:]
	site = site[:site.find('</span>')]
	print word+site

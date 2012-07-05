#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import HTMLParser
import re

h = HTMLParser.HTMLParser()

def parseHTML(html):
    return h.unescape(html)

def cleanHTML(html):
	return printable(re.sub(' +',' ',re.sub(r'<[^>]*>','',html))).strip(' ')

def printable(text):
	return re.sub('[\x00-\x1f]','',text)

# TODO this is some times very slow
def gethttp(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/4.0')]
		return ''.join(opener.open(url))
	except Exception as e:
		print 'EXCEPTION WITH URL "'+url+'"'
		print e
		return ''

def geturl(url):
	try:
		response = urllib2.urlopen(url)
		print response.geturl()
		''.join(response.geturl())
		return ''.join(response.geturl())
	except Exception as e:
		print 'EXCEPTION WITH URL "'+url+'"'
		print e
		return url 

def classContent(html, classname, type='class', end='<'):
	html = html[html.find(type+'="'+classname+'"'):]
	return html[html.find('>')+1 : html.find(end)]
	
'''def unescape(html):
	unescaped = ''
	for part in html.split('&#'):
		try:
			unescaped += chr(int(part.split(';')[0]))+part.split(';')[1]
		except:
			unescaped += part
	return unescaped'''

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import HTMLParser
import re

def messageUnescaped(connection, to, text):
	try:
		connection.message(to, h.unescape(text))
	except:
		connection.message(to, text)

def cleanHTML(html):
	return printable(re.sub(' +',' ',re.sub(r'<[^>]*>','',html))).strip(' ')

def printable(text):
	return re.sub('[\x00-\x1f]','',text)

def gethttp(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.1')]
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

def youtube(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.1')]
		youtube = ''.join(opener.open(url))
		title = youtube[youtube.find('<meta name="title" content="')+28:]
		title = cleanHTML(title[:title.find('">')])
		uploader = classContent(youtube, 'yt-user-name author')

		duration = youtube[youtube.find('<meta itemprop="duration" content="PT')+37:]
		duration = cleanHTML(duration[:duration.find('">')])
		minutes = duration[:duration.find('M')]
		seconds = duration[duration.find('M')+1:duration.find('S')]
		if int(minutes) > 59:
			hours = int(minutes)/60
			if int(minutes)%60 < 10:
				minutes = str(hours)+':0'+str(int(minutes)%60)
			else:
				minutes = str(hours)+':'+str(int(minutes)%60)
		if int(seconds) < 10:
			seconds = '0'+seconds
			
		views = cleanHTML(classContent(youtube, 'watch-view-count', 'class', '</span>'))
		likes = classContent(youtube, 'likes')
		dislikes = classContent(youtube, 'dislikes')
		return '\00300,01[You\00304Tube\00300]\003 \002'+title+'\002 \00311('+minutes+':'+seconds+\
		') \00312by '+uploader+'\00314\002\002, \00309'+likes+' likes\00314\002\002, \00304'\
		+dislikes+' dislikes\00314\002\002, \00308'+views+' views'
	except Exception as e:
		print 'EXCEPTION WITH YOUTUBE "'+url+'"'
		print e
		return ''

def fweather(FUCKINGPLACE):
	try:
		FUCKINGOPENER = urllib2.build_opener()
		FUCKINGOPENER.addheaders = [('User-agent', 'FUCKING NUX/3.1')]
		if len(FUCKINGPLACE) > 1:
			FUCKINGPLACE = FUCKINGPLACE[1:]
			FUCKINGDATA = ''.join(FUCKINGOPENER.open('http://thefuckingweather.com/?where='+
			urllib2.quote(FUCKINGPLACE)+'&unit=c'))
		else:
			FUCKINGDATA = ''.join(FUCKINGOPENER.open('http://thefuckingweather.com/?unit=c&random=True'))		
		FUCKINGHTMLPARSER = HTMLParser.HTMLParser()
		FUCKINGWEATHER = FUCKINGDATA[FUCKINGDATA.find('<div class="content">')+21:FUCKINGDATA.find('</>')]

		if FUCKINGDATA.find('I CAN&#39;T FIND THAT SHIT') == -1:
			FUCKINGTEMPERATURE = cleanHTML(classContent(FUCKINGWEATHER, 'temperature', 'class', '</p>'))
			FUCKINGLOCATION = classContent(FUCKINGDATA, 'locationDisplaySpan', 'id')
			print 'FUCKING WEATHER IN '+FUCKINGLOCATION
			FUCKINGREMARK = classContent(FUCKINGWEATHER, 'remark')
			FUCKINGFLAVOR = classContent(FUCKINGWEATHER, 'flavor')
			
			return unescape('\00312['+FUCKINGLOCATION+'] \00304\002'+FUCKINGTEMPERATURE+' \00308'
			+FUCKINGREMARK+' \002\00311['+FUCKINGFLAVOR+']')

		else:
			return unescape('\002\00304INVALID FUCKING LOCATION')
						
	except Exception as FUNCKINGEXCEPTION:
		print 'FUCKING EXCEPTION WITH THE FUCKING WEATHER IN "'+FUCKINGPLACE+'"'
		print FUNCKINGEXCEPTION
		return unescape('\002\00304INVALID FUCKING LOCATION')

def calc(expression):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.1')]
		google = ''.join(opener.open('http://www.google.com/search?q='+
			urllib2.quote(expression)))
		print google
		if google.find('<h2 class="r" dir="ltr"') != -1:
			answer = google[google.find('class="r" dir="ltr"'):]
			answer = answer[answer.find('>')+1:answer.find('<')]
			return unescape('\00300[\00312G\00304o\00308o\00312g\00309l\00304e\00300] \002'
			+answer)
		else:
			return unescape('\00300[\00312G\00304o\00308o\00312g\00309l\00304e\00300] \002'
			+'\00304Could not calculate!')


	except Exception as e:
		print 'EXCEPTION WITH CALCULATION "'+expression+'"'
		print e
		return unescape('\00300[\00312G\00304o\00308o\00312g\00309l\00304e\00300] '
		+'\00304COULD NOT CALCULATE')

def classContent(html, classname, type='class', end='<'):
	html = html[html.find(type+'="'+classname+'"'):]
	return html[html.find('>')+1 : html.find(end)]
	
def unescape(html):
	unescaped = ''
	for part in html.split('&#'):
		try:
			unescaped += chr(int(part.split(';')[0]))+part.split(';')[1]
		except:
			unescaped += part
	return unescaped
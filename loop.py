#!/usr/bin/python
# -*- coding: UTF-8 -*-

import irc
#import url
import os
import urllib2
#import httplib
import HTMLParser
import re
import time
import random

h = HTMLParser.HTMLParser()

def geturl(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.0')]
		return ''.join(opener.open(url))
	except Exception as e:
		print 'EXECTION WITH URL "'+url+'"'
		print e
		return ''

def printable(text):
	return re.sub('[\x00-\x1f]','',text)

def messageUnescaped(irc, to, text):
	try:
		irc.message(to, h.unescape(text))
	except:
		irc.message(to, text)
		
def cleanHTML(html):
	return printable(re.sub(r'<[^>]*>','',html)).strip(' ')
	
def parseYouTube(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.0')]
		youtube = ''.join(opener.open(url))
		title = youtube[youtube.find('<meta name="title" content="')+28:]
		title = cleanHTML(title[:title.find('">')])
		uploader = youtube[youtube.find('class="yt-user-name author" rel="author" dir="ltr">')+51:]
		uploader = cleanHTML(uploader[:uploader.find('</span>')])
		if uploader.find(', ') != -1:
			uploader = uploader[:uploader.find(', ')]
		print uploader
		
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
			
		views = youtube[youtube.find('class="watch-view-count">')+25:]
		views = cleanHTML(views[:views.find('</span>')])
		likes = youtube[youtube.find('class="likes">')+14:]
		likes = cleanHTML(likes[:likes.find('</span>')])
		dislikes = youtube[youtube.find('class="dislikes">')+17:]
		dislikes = cleanHTML(dislikes[:dislikes.find('</span>')])
		return '\00300[You\00304Tube\00300] \002'+title+'\002 \00310('+minutes+':'+seconds+') \00312by '+uploader+'\00301, \00309'+likes+' likes\00301, \00304'+dislikes+' dislikes\00301, \00308'+views+' views'
	except Exception as e:
		print 'EXECTION WITH YOUTUBE "'+url+'"'
		print e
		return ''

# returns True if needs to be reloaded
def cycle(irc):
	reload = False
	ircmsg = irc.recv().strip('\n\r')
	for line in ircmsg.split('\n'):
		print '>'+line			
		linesplit = line.split()

		# it doesn't matter if nux sends unnecessary PONGs
		# but it does matter if any PING is ignored
		if line.startswith('PING :'):
			irc.send('PONG :'+line.split('PING :')[1])
			continue
		
		nick = ''
		action = ''
		if line.split()[0].find('!') != -1:
			nick = line[1:].split('!')[0]
			action = line.split()[1]
		if action == 'PRIVMSG':
			msg = line[line[1:].find(':')+2:]
			if len(msg.split()) > 0:
				cmd = msg.split()[0]

			arg = ''
			if msg.find(' ') != -1:
				arg = msg[msg.find(' ')+1:]
				
			sender = nick
			if linesplit[2][0] == '#' or linesplit[2][0] == '&':
				sender = linesplit[2]
			
			# God commands
			if irc.isGod(nick):
				# join a channel
				if cmd == '!join':
					if arg:
						irc.join(arg.split()[0])

				# part from a channel
				elif cmd == '!part':
					if arg:
						irc.part(arg, nick)
					else:
						irc.part(sender, nick)

				# (rage)quit
				elif cmd == '!quit':
					if arg:
						irc.send('QUIT :killed by '+nick+' ('+arg+')')
					else:
						irc.send('QUIT :killed by '+nick)
					quit()

				# change channel mode
				elif cmd == '!mode' and arg:
					if arg[0] == '#' or arg[0] == '&':
						irc.send('MODE '+arg)
					else:
						irc.send('MODE '+sender+' '+arg)

				# add or list gods
				elif cmd == '!god':
					if arg:
						for god in arg.split():
							irc.addGod(god)
					else:
						irc.message(sender, irc.getGods())

				# remove a god
				elif cmd == '!devil':
					if arg:
						for god in arg.split():
							irc.removeGod(god)

				# reload modules
				elif cmd == '!reload':
					reload = True
					continue
					
				# delay between PRIVMSGs
				elif cmd == '!delay':
					if arg:
						try:
							irc.setDelay(float(arg))
						except ValueError:
							pass
					else:
						irc.message(sender, str(irc.getDelay()))

			# Non god commands
										
			if cmd == '!reset':
				try:
					irc.addGod(open('god.txt').read())
					open('god.txt', 'w').writelines('')
				except:
					pass

			elif cmd == '!help':
				irc.message(sender, '!help !ud !day !wa !maze')

			# Urban Dictionary
			elif cmd == '!ud':
				data = geturl('http://www.urbandictionary.com/define.php?term='
				+ urllib2.quote(arg)).split("\n")
				answer = "ei tuloksia"
				for line in data:
					if line.find('class="definition"') != -1:
						answer = re.sub(r'<[^>]*>','',line)
						break
				messageUnescaped(irc, sender, answer)

			# What's special in today
			elif cmd == '!day':
				date = time.strftime('%B_%e').replace(' ','')
				data = geturl('http://en.wikipedia.org/wiki/'+date).split('\n')
				fun = []
				add = False
				for line in data:
					if add:
						if line.find(' Births') != -1:
							break
						else:
							fun.append(re.sub(r'<[^>]*>','',line))
					if line.find(' Events') != -1:
						add = True
						
				# if `date +%-d.%-m.` outputs '-d.-m.', replace '%-d.%-m.' with '%d.%m.'
				irc.message(sender, time.strftime('%-d.%-m.') + random.choice(fun[1:-1]))

			# Wolfram|Alpha
			elif cmd == '!wa':
				result = "ei tuloksia"
				wa = geturl('http://www.wolframalpha.com/input/?i='+urllib2.quote(arg)).split('\n')
				n = 0
				for line in wa:
					if line.find('stringified') != -1:
						n+=1
						if(n == 2):
							result = line.split('"')[ 3 ].replace("\\n","\r\n")
				# todo: make a nice array
				messageUnescaped(irc, sender, result)

			if msg.find('://') != -1:
				url = msg[max(0, msg[:msg.find('://')].rfind(' ')+1):]
				protocol = url[:url.find('://')]
				if protocol == 'http' or protocol == 'https':
					if url.find(' ') != -1:
						url = url[:url.find(' ')]
					print 'URL = '+url
					data = geturl(url)
					if url.startswith('http://www.youtube.com/watch'):
						irc.message(sender, parseYouTube(url))
					else:
						if data.find('<title>') != -1 and data.find('</title>') != -1:
							title = re.sub(r'<[^>]*>','',data[data.find('<title>')+7:data.find('</title>')])
							messageUnescaped(irc, sender, 'Title: '+cleanHTML(title))
						else:
							irc.message(sender, 'No title')
				else:
					print 'unknown protocol ('+protocol+')'
					
			# Maze
			if cmd == '!maze':
				print '"'+arg+'"'
				try:
					x = int(arg[:arg.find('x')])
					print x
					y = int(arg[arg.find('x')+1:])
					print y
					if irc.isGod(nick):
						if y > 40 or x > 63:
							irc.message(sender, 'suurin koko on 63x40')
					else:
						if y > 10 or x > 30:
							irc.message(sender, 'suurin koko on 30x10')

					if x < 3 or y < 3:
						irc.message(sender, 'pienin koko on 3x3')
					else:
						maze = os.popen('java Generator '+str(x)+' '+str(y)+' | ./box.sh').read()
						if irc.isGod(nick) or y < 6:
							irc.message(sender, maze)
						else:
							irc.message(nick, maze)
				except ValueError:
					irc.message(sender, 'syntaksi: !maze <leveys>x<korkeus>')
				except IndexError:
					irc.message(sender, 'syntaksi: !maze <leveys>x<korkeus>')

			
		# Join if invited
		elif action == 'INVITE':
			irc.godMessage(nick+' kutsui minut kanavalle '+linesplit[3][1:])
			if linesplit[3][1] == '#' or linesplit[3][1] == '&':
				irc.join(linesplit[3][1:])
				
		# Keep gods list updated
		elif action == 'NICK':
			if irc.isGod(nick):
				irc.removeGod(nick)
				irc.addGod(linesplit[2][1:])
		
		# Cycle if not operator and alone on a channel
		elif action == 'PART':
			sender = linesplit[2]
			irc.send('NAMES '+sender)
			line = irc.recv().strip('\r\n')
			names = line.split(':')[2].split()
			if len(names) == 1:
				if names[0][0] == 'n' or names[0][0] == '+' or names[0][0] == '%':
					print line.split(':')
					print line.split(':')[2].split()
					irc.part(sender, nick)
					irc.join(sender)
					irc.godMessage('valtasin kanavan '+sender)
		
		# Auto rejoin
		elif action == 'KICK':
			irc.join(line.split()[2])
			
		# Protect self from hackers
		elif action == 'QUIT':
			nick = line[1:line.find('!')]
			if irc.isGod(nick):
				print 'GOD HAS QUIT ('+nick+')'
				irc.removeGod(nick) # god.txt

	return reload

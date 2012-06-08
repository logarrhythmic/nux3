#!/usr/bin/python
# -*- coding: UTF-8 -*-

import irc
import os
import urllib2
import HTMLParser
import re
import time
import random
import imp

h = HTMLParser.HTMLParser()

def gethttp(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.0')]
		return ''.join(opener.open(url))
	except Exception as e:
		print 'EXECTION WITH URL "'+url+'"'
		print e
		return ''

def geturl(url):
	try:
		response = urllib2.urlopen(url)
		print response.geturl()
		''.join(response.geturl())
		return ''.join(response.geturl())
	except Exception as e:
		print 'EXECTION WITH URL "'+url+'"'
		print e
		return url


def printable(text):
	return re.sub('[\x00-\x1f]','',text)

def messageUnescaped(connection, to, text):
	try:
		connection.message(to, h.unescape(text))
	except:
		connection.message(to, text)
		
def cleanHTML(html):
	return printable(re.sub(' +',' ',re.sub(r'<[^>]*>','',html)).strip(' '))
	
def parseYouTube(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.0')]
		youtube = ''.join(opener.open(url))
		title = youtube[youtube.find('<meta name="title" content="')+28:]
		title = cleanHTML(title[:title.find('">')])
		uploader = youtube[youtube.find('class="yt-user-name author" rel="author" dir="ltr">')+51:]
		uploader = cleanHTML(uploader[:uploader.find('</a>')])
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
		return '\00300[You\00304Tube\00300] \002'+title+'\002 \00311('+minutes+':'+seconds+') \
		\00312by '+uploader+'\00314\002\002, \00309'+likes+' likes\00314\002\002, \
		\00304'+dislikes+' dislikes\00314\002\002, \00308'+views+' views'
	except Exception as e:
		print 'EXECTION WITH YOUTUBE "'+url+'"'
		print e
		return ''

# returns True if needs to be reloaded
def cycle(connection):
	reloadModules = False
	ircmsg = connection.recv().strip('\n\r')
	for line in ircmsg.split('\n'):
		print '>'+line			
		linesplit = line.split()

		# it doesn't matter if nux sends unnecessary PONGs
		# but it does matter if any PING is ignored
		if line.startswith('PING :'):
			connection.send('PONG :'+line.split('PING :')[1])
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
			if connection.isGod(nick):
				# join a channel
				if cmd == '!join' and arg:
					for channel in arg.split():
						connection.join(channel)

				# part from a channel
				elif cmd == '!part':
					if arg:
						for channel in arg.split():
							connection.part(channel, nick)
					else:
						connection.part(sender, nick)

				# (rage)quit
				elif cmd == '!quit':
					if arg:
						connection.send('QUIT :killed by '+nick+' ('+arg+')')
					else:
						connection.send('QUIT :killed by '+nick)
					quit()

				# change channel mode
				elif cmd == '!mode' and arg:
					if arg[0] == '#' or arg[0] == '&':
						connection.send('MODE '+arg)
					else:
						connection.send('MODE '+sender+' '+arg)

				# add or list gods
				elif cmd == '!god':
					if arg:
						for god in arg.split():
							connection.addGod(god)
					else:
						connection.message(sender, connection.getGods())

				# remove a god
				elif cmd == '!devil':
					if arg:
						for god in arg.split():
							connection.removeGod(god)

				# reload modules
				elif cmd == '!reload':
					reloadModules = True
					reload(irc)
					copy = getattr(irc, 'Irc')
					connection.__class__ = copy
					continue
					
				# delay between PRIVMSGs
				elif cmd == '!delay':
					if arg:
						try:
							connection.setDelay(float(arg))
						except ValueError:
							pass
					else:
						connection.message(sender, str(connection.getDelay()))

			# Non god commands
										
			if cmd == '!reset':
				try:
					connection.addGod(open('god.txt').read())
					open('god.txt', 'w').writelines('')
				except:
					pass

			elif cmd == '!help':
				connection.message(sender, '!help !ud !day !wa !maze')

			# Urban Dictionary
			elif cmd == '!ud':
				data = gethttp('http://www.urbandictionary.com/define.php?term='\
				+urllib2.quote(arg)).split("\n")
				answer = "ei tuloksia"
				for line in data:
					if line.find('class="definition"') != -1:
						answer = re.sub(r'<[^>]*>','',line)
						break
				messageUnescaped(connection, sender, answer)

			# What's special in today
			elif cmd == '!day':
				date = time.strftime('%B_%e').replace(' ','')
				data = gethttp('http://en.wikipedia.org/wiki/'+date).split('\n')
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
				connection.message(sender, time.strftime('%-d.%-m.') + random.choice(fun[1:-1]))

			# Wolfram|Alpha
			elif cmd == '!wa':
				result = "ei tuloksia"
				wa = gethttp('http://www.wolframalpha.com/input/?i='\
				+urllib2.quote(arg)).split('\n')
				n = 0
				for line in wa:
					if line.find('stringified') != -1:
						n+=1
						if(n == 2):
							result = line.split('"')[ 3 ].replace("\\n","\r\n")
				# todo: make a nice array
				messageUnescaped(connection, sender, result)

			if msg.find('://') != -1:
				url = msg[max(0, msg[:msg.find('://')].rfind(' ')+1):]
				protocol = url[:url.find('://')]
				if protocol == 'http' or protocol == 'https':
					if url.find(' ') != -1:
						url = url[:url.find(' ')]
					print 'URL = '+url
					data = gethttp(url)
					realurl = geturl(url)
					if realurl.startswith('http://www.youtube.com/watch'):
						connection.message(sender, parseYouTube(url))
					else:
						if data.find('<title>') != -1 and data.find('</title>') != -1:
							title = re.sub(r'<[^>]*>','',\
							data[data.find('<title>')+7:data.find('</title>')])
							if realurl != url:
								realurl = realurl[realurl.find('://')+3:]
								realurl = realurl[:realurl.find('/')]
								messageUnescaped(connection, sender, 'Title: '+cleanHTML(title)+' \
								\00315(at \00310\002'+realurl+'\002\00315)')
							else:
								messageUnescaped(connection, sender, 'Title: '+cleanHTML(title))
						else:
							connection.message(sender, 'No title')
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
					if connection.isGod(nick):
						if y > 40 or x > 63:
							connection.message(sender, 'suurin koko on 63x40')
					else:
						if y > 10 or x > 30:
							connection.message(sender, 'suurin koko on 30x10')

					if x < 3 or y < 3:
						connection.message(sender, 'pienin koko on 3x3')
					else:
						maze = os.popen('java Generator '+str(x)+' '+str(y)+' | ./box.sh').read()
						if connection.isGod(nick) or y < 6:
							connection.message(sender, maze)
						else:
							connection.message(nick, maze)
				except ValueError:
					connection.message(sender, 'syntaksi: !maze <leveys>x<korkeus>')
				except IndexError:
					connection.message(sender, 'syntaksi: !maze <leveys>x<korkeus>')

			
		# Join if invited
		elif action == 'INVITE':
			connection.godMessage(nick+' kutsui minut kanavalle '+linesplit[3][1:])
			if linesplit[3][1] == '#' or linesplit[3][1] == '&':
				connection.join(linesplit[3][1:])
				
		# Keep gods list updated
		elif action == 'NICK':
			if connection.isGod(nick):
				connection.removeGod(nick)
				connection.addGod(linesplit[2][1:])
		
		# Cycle if not operator and alone on a channel
		elif action == 'PART':
			sender = linesplit[2]
			connection.send('NAMES '+sender)
			line = connection.recv().strip('\r\n')
			names = line.split(':')[2].split()
			if len(names) == 1:
				if names[0][0] == 'n' or names[0][0] == '+' or names[0][0] == '%':
					print line.split(':')
					print line.split(':')[2].split()
					connection.part(sender, nick)
					connection.join(sender)
					connection.godMessage('valtasin kanavan '+sender)
		
		# Auto rejoin
		elif action == 'KICK':
			connection.join(line.split()[2])
			
		# Protect self from hackers
		elif action == 'QUIT':
			nick = line[1:line.find('!')]
			if connection.isGod(nick):
				print 'GOD HAS QUIT ('+nick+')'
				connection.removeGod(nick) # god.txt

	return reloadModules

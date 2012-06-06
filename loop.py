#!/usr/bin/python
# -*- coding: UTF-8 -*-

import irc
#import url
import os
import urllib2
#import urllib
#import httplib
#import HTMLParser
import re

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


# returns True if needs to be reloaded
def cycle(irc):
	reload = False
	ircmsg = irc.recv().strip('\n\r')
	for line in ircmsg.split('\n'):
		print '>'+line			
		linesplit = line.split()
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
				if cmd == '!god':
					if arg:
						for god in arg.split():
							irc.addGod(god)
					else:
						irc.message(sender, irc.getGods())

				# remove a god
				if cmd == '!devil':
					if arg:
						for god in arg.split():
							irc.removeGod(god)

				# reload modules
				if cmd == '!reload':
					reload = True
#					reload(url)
					irc.addGod(open('god.txt').read())
					open('god.txt', 'w').writelines('')
					continue
				
			if cmd == '!help':
				irc.message(sender, '!help !day')

			if msg.find('://') != -1:
				url = msg[max(0, msg[:msg.find('://')].rfind(' ')+1):]
				protocol = url[:url.find('://')]
				if protocol == 'http' or protocol == 'https':
					if url.find(' ') != -1:
						url = url[:url.find(' ')]
					print 'URL = '+url
					data = geturl(url)
					if data.find('<title>') != -1 and data.find('</title>') != -1:
						title = re.sub(r'<[^>]*>','',data[data.find('<title>')+7:data.find('</title>')])
						irc.message(sender, 'Title: '+printable(title))
					else:
						irc.message(sender, 'No title')
				else:
					print 'unknown protocol ('+protocol+')'
			
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

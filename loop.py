#!/usr/bin/python
# -*- coding: UTF-8 -*-

import irc
import http
import os
import urllib2
import HTMLParser
import re
import time
import random
import imp
import log

h = HTMLParser.HTMLParser()

def printable(text):
	return re.sub('[\x00-\x1f]','',text)

def messageUnescaped(connection, to, text):
	try:
		connection.message(to, h.unescape(text))
	except:
		connection.message(to, text)

# returns True if needs to be reloaded
def cycle(connection, channels):
	reloadModules = False
	ircmsg = connection.recv()
	for line in ircmsg:
		linesplit = line.split()

		# it doesn't matter if nux sends unnecessary PONGs
		# but it does matter if any PING is ignored
		if line.startswith('PING :'):
			connection.send('PONG :'+line.split('PING :')[1])
			continue

		if line.startswith('VERSION :'):
			connection.send('VERSION :nux 3.1')
			continue
		
		nick = ''
		action = ''
		if line.split()[0].find('!') != -1:
			nick = line[1:].split('!')[0]
			action = line.split()[1]
		if action == 'PRIVMSG':
			msg = line[line[1:].find(':')+2:]
			cmd = ''
			if len(msg.split()) > 0:
				cmd = msg.split()[0]

			arg = ''
			if msg.find(' ') != -1:
				arg = msg[msg.find(' '):]
				if arg:
					arg = arg[1:]
				
			sender = nick
			if linesplit[2][0] == '#' or linesplit[2][0] == '&':
				sender = linesplit[2]
						
			# s//
			if msg.startswith('s/') and msg[2:].find('/') != -1:
				if msg.count('/') == 2:
					quote = channels.getMessage(sender, msg[2:msg.rfind('/')])
					if quote:
						new = re.sub(msg[2:msg[2:].find('/')+2],
						msg[msg[2:].find('/')+3:], ' '.join(quote.split()[1:]), 1)
						new = new.replace('\n', '')
						
						print quote
						print msg
		
						# /me
						if new.startswith('\001ACTION '):
							new = new.strip('\001')[7:]
							print '* '+quote.split()[0]+' '+new
							connection.message(sender, '\002* '+quote.split()[0]+'\002 '+new)
						# normal
						else:
							print '<'+quote.split()[0]+'> '+new
							connection.message(sender, '<\002'+quote.split()[0]+'\002> '+new)

				# s///g
				elif msg.count('/') == 3 and msg[msg.rfind('/'):] == '/g':
					quote = channels.getMessage(sender, msg[2:msg[2:].find('/')+2])
					if quote:
						new = re.sub(msg[2:msg[2:].find('/')+2],
						msg[msg[2:].find('/')+3:msg.rfind('/')],
						' '.join(quote.split()[1:]))
						new = new.replace('\n', '')

						print quote
						print msg
		
						# /me
						if new.startswith('\001ACTION '):
							new = new.strip('\001')[7:]
							print '* '+quote.split()[0]+' '+new
							connection.message(sender, '\002* '+quote.split()[0]+'\002 '+new)
						# normal
						else:
							print '<'+quote.split()[0]+'> '+new
							connection.message(sender, '<\002'+quote.split()[0]+'\002> '+new)

			else:
				channels.addMessage(sender, nick, msg)


			helpFound = True
			
			# God commands
			if connection.isGod(nick):
				# join a channel
				if cmd == '!join' and arg:
					for channel in arg.split():
						connection.join(channel)
						channels.addChannel(channel)

				# part from a channel
				elif cmd == '!part':
					if arg:
						for channel in arg.split():
							connection.part(channel, nick)
							channels.removeChannel(channel)
					else:
						connection.part(sender, nick)
						channels.removeChannel(sender)

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
				elif cmd == '!devil' and arg:
					for god in arg.split():
						connection.removeGod(god)

				# reload modules
				elif cmd == '!reload':
					reloadModules = True
					reload(http)
					reload(irc)
#					reload(log)
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
						connection.message(sender, 'viive on '+str(connection.getDelay())+'s')

				# Say
				elif cmd == '!say' and len(arg.split()) > 1:
					connection.message(arg.split()[0], arg[arg.find(' ')+1:])


				elif cmd == '!help':
					if not arg:
						connection.notice(nick,
						'-- Jumalille --\n'
						'    !delay !devil !god !join !mode !part !quit !reload !say\n'
						'-- Kaikille --\n'
						'    !calc !day !help !maze (!reset) !ud !wa sed')
					elif arg == '!delay' or arg == 'delay':
						connection.notice(nick,
						'!delay <float>\n'
						'    Asettaa viiveen viestien välille (sekunteina).\n'
						'!delay\n'
						'    Kertoo asetetun viiveen.')
					elif arg == '!devil' or arg == 'devil':
						connection.notice(nick,
						'!devil <nick>\n'
						'    Poistaa <nick>:n jumalallisesta listasta.')
					elif arg == '!god' or arg == 'god':
						connection.notice(nick,
						'!god <nick>\n'
						'    Lisää <nick>:n jumalalliselle listalle. Jumalat pääsevät\n'
						'    käsiksi kaikkiin komentoihin.\n'
						'!god\n'
						'    Kertoo jumalallisen listan.')
					elif arg == '!join' or arg == 'join':
						connection.notice(nick,
						'!join <channel1> [<channel2> [...]]\n'
						'    Liittyy kaikille kanaville (mille mahdollista).')
					elif arg == '!mode' or arg == 'mode':
						connection.notice(nick,
						'!mode <channel> <mode>\n'
						'    Muuttaa kanavan <channel> moodia.\n'
						'!mode <mode>\n'
						'    Muuttaa nykyisen kanavan moodia.')
					elif arg == '!part' or arg == 'part':
						connection.notice(nick,
						'!part <channel>\n'
						'    Poistuu kanavalta <channel>.\n'
						'!part\n'
						'    Poistuu nykyiseltä kanavalta.')
					elif arg == '!quit' or arg == 'quit':
						connection.notice(nick,
						'!quit [<reason>]\n'
						'    QUIT :killed by <nick>[ (<reason>)]')
					elif arg == '!reload' or arg == 'reload':
						connection.notice(nick,
						'!reload\n'
						'    Lataa moduulit uudestaan. Tarpeellinen jos on uusia\n'
						'    päivityksiä.')
					elif arg == '!say' or arg == 'say':
						connection.notice(nick,
						'!say <channel> <message>\n'
						'    sanoo kanavalle jotain (toimii myös queryyn).\n'
						'    PRIVMSG <channel> :<message>')
					elif arg == '!reset' or arg == 'reset':
						connection.notice(nick,
						'!reset\n'
						'    Lisää jumalalliseen listaan nikin tiedostosta god.txt.\n'
						'    Ei normaaliin käyttöön.')
					else:
						helpFound = False

			else:
				if cmd == '!help' and not arg:
					connection.notice(nick, '!calc !day !help !maze !ud !wa sed')
	
			if cmd == '!help' and arg and not helpFound:
				if arg == '!day' or arg == 'day':
					date = time.strftime('%B_%e').replace(' ','')
					connection.notice(nick,
					'!day\n'
					'    Mitä tänään tapahtui n vuotta sitten.\n'
					'    http://en.wikipedia.org/wiki/'+date)
				elif arg == '!help' or arg == 'help':
					connection.notice(nick,
					'!help\n'
					'    Lista komennoista.\n'
					'!help <cmd>\n'
					'    Komennon <cmd> manuaali.')
				elif arg == '!maze' or arg == 'maze':
					connection.notice(nick,
					'!maze <leveys>x<korkeus>\n'
					'    Tulostaa nykyiselle kanavalle (tai queryyn) sokkelon.')
				elif arg == '!ud' or arg == 'ud':
					connection.notice(nick,
					'!ud <sana>\n'
					'    Hakee sanan selityksen osoitteesta\n'
					'    http://www.urbandictionary.com/define.php?term=<sana>')
				elif arg == '!wa' or arg == 'wa':
					connection.notice(nick,
					'!wa <lasku tai kysymys>\n'
					'    Wolfram|Alpha\n'
					'    http://www.wolframalpha.com/')
				elif arg == 'sed':
					connection.notice(nick,
					's/<regexp1>/<regexp2>[/g]\n'
					'    Etsii viimeisen kymmenen rivin joukosta viimeisen\n'
					'    rivin joka vastaa <rexegp1> kuviota ja korvaa ensimmäisen\n'
					'    esiintymän <regexp2> kuviolla. Jos /g on asetettu niin\n'
					'    kaikki esiintymät korvataan.')
				elif arg == '!calc' or arg == 'calc':
					connection.notice(nick,
					'!calc <lasku>\n'
					'    Googlen laskin, \n'
					'    https://www.google.fi/intl/fi/help/features.html#calculator')
				else:
					connection.notice(nick, 'Ei apua.')


			# Non god commands
										
			if cmd == '!reset':
				try:
					connection.addGod(printable(open('god.txt').read()))
					open('god.txt', 'w').writelines('')
				except:
					pass


			# Urban Dictionary
			elif cmd == '!ud':
				data = http.gethttp('http://www.urbandictionary.com/define.php?term='\
				+urllib2.quote(arg)).split("\n")
				answer = "ei tuloksia"
				for line in data:
					if line.find('class="definition"') != -1:
						answer = re.sub(r'<[^>]*>','',line)
						break
				try:
					connection.message(sender, h.unescape(answer))
				except:
					connection.message(sender, answer)

			# What's special in today
			elif cmd == '!day':
				date = time.strftime('%B_%e').replace(' ','')
				data = http.gethttp('http://en.wikipedia.org/wiki/'+date).split('\n')
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
				connection.message(sender, random.choice(fun[1:-1]))

			# Wolfram|Alpha
			elif cmd == '!wa':
				result = "ei tuloksia"
				wa = http.gethttp('http://www.wolframalpha.com/input/?i='\
				+urllib2.quote(arg)).split('\n')
				n = 0
				for line in wa:
					if line.find('stringified') != -1:
						n+=1
						if(n == 2):
							result = line.split('"')[ 3 ].replace("\\n","\r\n")
				# todo: make a nice array
				messageUnescaped(connection, sender, result)
				
			# Fucking weather
			elif cmd == '!fweather':
				messageUnescaped(connection, sender, http.fweather(msg[9:]))

			# Calculate using Google
			elif cmd == '!calc':
				connection.message(sender, http.calc(msg[5:]))

			if msg.find('://') != -1:
				url = msg[max(0, msg[:msg.find('://')].rfind(' ')+1):]
				protocol = url[:url.find('://')]
				if protocol == 'http' or protocol == 'https':
					if url.find(' ') != -1:
						url = url[:url.find(' ')]
					print 'URL = '+url
					data = http.gethttp(url)
					realurl = http.geturl(url)
					if realurl.startswith('http://www.youtube.com/watch'):
						connection.message(sender, http.youtube(url))
					else:
						if data.find('<title>') != -1 and data.find('</title>') != -1:
							title = re.sub(r'<[^>]*>','',\
							data[data.find('<title>')+7:data.find('</title>')])
							if realurl != url:
								realurl = realurl[realurl.find('://')+3:]
								realurl = realurl[:realurl.find('/')]
								connection.message(sender, 'Title: '
								+printable(http.unescape(http.cleanHTML(title)))
								+' \00315(at \00310\002'+realurl+'\002\00315)')
							else:
								connection.message(sender, 'Title: '
								+printable(http.unescape(http.cleanHTML(title))))
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
							continue
						elif x < 3 or y < 3:
							connection.message(sender, 'pienin koko on 3x3')
						else:
							maze = os.popen('java Generator '+str(x)+' '+str(y)+' | ./box.sh').read()
							connection.message(sender, maze)
					else:
						if y > 10 or x > 30:
							connection.message(sender, 'suurin koko on 30x10')
							continue

						elif x < 3 or y < 3:
							connection.message(sender, 'pienin koko on 3x3')
						else:
							maze = os.popen('java Generator '+str(x)+' '+str(y)+' | ./box.sh').read()
							if y < 6:
								connection.message(sender, maze)
							else:
								connection.message(nick, maze)
				except ValueError:
					connection.message(sender, 'syntaksi: !maze <leveys>x<korkeus>')
				except IndexError:
					connection.message(sender, 'syntaksi: !maze <leveys>x<korkeus>')
					
			if msg.lower() == 'ok':
				connection.message(sender, '/kick '+nick)
				
			# CTCPs
			if msg[0] == '\001' and msg[-1] == '\001' and not msg[1:].startswith('ACTION'):
				msg = msg.strip('\001')
				if msg == 'VERSION':
					print 'CTCP VERSION request from '+nick
					connection.notice(nick, '\001VERSION nux v3.1\001')
				if msg.startswith('PING '):
					print 'CTCP PING request from '+nick
					connection.notice(nick, '\001PING '+msg[5:]+'\001')
				else:
					print 'Unknown CTCP '+msg+' request from '+nick					
			
		# Join if invited
		elif action == 'INVITE':
			connection.godMessage(nick+' kutsui minut kanavalle '+linesplit[3][1:])
			if linesplit[3][1] == '#' or linesplit[3][1] == '&':
				connection.join(linesplit[3][1:])
				channels.addChannel(linesplit[3][1:])
				
		# Keep gods list updated
		elif action == 'NICK':
			if connection.isGod(nick):
				connection.removeGod(nick)
				connection.addGod(linesplit[2][1:])
		
		# Cycle if not operator and alone on a channel
		elif action == 'PART':
			sender = linesplit[2]
			connection.send('NAMES '+sender)
			for line in ircmsg:
				print line
				if len(line.split()) > 1 and len(line.split(':')) > 1:
					if line.find(sender+' :') != -1 and line.split()[2] == 'nux':
						names = line.split(':')[2].split()
						print names
						if len(names) == 1:
							if names[0][0] == 'n' or names[0][0] == '+' or names[0][0] == '%':
								print line.split(':')
								print line.split(':')[2].split()
								connection.part(sender, nick)
								connection.join(sender)
								connection.godMessage('valtasin kanavan '+sender)
		
		#Autojoin
			
		# Protect self from hackers
		elif action == 'QUIT':
			nick = line[1:line.find('!')]
			if connection.isGod(nick):
				print 'GOD HAS QUIT ('+nick+')'
				connection.removeGod(nick) # god.txt

	return reloadModules

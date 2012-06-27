#!/usr/bin/python
# -*- coding: UTF-8 -*-

import irc
import http
import urllib2
import HTMLParser
import re
import time
import random
import imp

version = 'nux v4.0'

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
			connection.send('VERSION :'+version)
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
					copy = getattr(irc, 'Irc')
					connection.__class__ = copy
					continue

			# Non god commands
			if cmd == '!reset':
				try:
					connection.addGod(printable(open('god.txt').read()))
					open('god.txt', 'w').writelines('')
				except:
					pass

			# CTCPs
			if msg[0] == '\001' and msg[-1] == '\001' and not msg[1:].startswith('ACTION'):
				msg = msg.strip('\001')
				if msg == 'VERSION':
					print 'CTCP VERSION request from '+nick
					connection.notice(nick, '\001VERSION '+version+'\001')
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
		
		# Auto rejoin
		elif action == 'KICK':
			connection.join(line.split()[2])
			
		elif action == 'QUIT':
			nick = line[1:line.find('!')]
			if connection.isGod(nick):
				print 'GOD HAS QUIT ('+nick+')'
				connection.removeGod(nick) # god.txt

	return reloadModules


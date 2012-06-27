#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import inspect_shell
import socket
import time
import sys
import log

class Irc:
	def __init__(self, network, serverport, nickname, realname):
		self.network = network
		self.serverport = serverport
		self.gods = []
		self.authenticated = False
		self.nickname = nickname
		
		# connect to IRC
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((network, serverport))
		self.send('NICK '+nickname)
		self.send('USER '+nickname+' host irc-server :'+realname)
		self.delay = 0
		self.commands = [modules.help.help()]
		
	def cycle(self):
		line = self.recv()
		if line[1] == ':':
			sender = line.split()[0][1:]
			command = line.split()[1]
			if command = 'PRIVMSG':
				user = line.split()[0][1:]
				destination = line.split()[2]
				message = line[line[1:].find(':')+2:]
				if destination = self.nickname:
					destination = nick
#				if message[0]
				for command in self.commands:
					command(self, user, destination, message)
		else:
			command = line.split()[0]
			if command = 'PING':
				self.send('PONG '+line[5:])

	def recv(self):
		# receive one character at time until "\n"
		data = ""
		while 1:
			character = self.connection.recv(1)
			if character:
				# only receive one line at time
				if character == '\n':
					break
				if character != '\r':
					data += character
			else:
				raise RuntimeException("Connection closed")
		print '>'+data
		return data

	def send(self, data):
		data = data[:data.find('\n')]
		if len(data) > 396:
			data = data[:data[:400].rfind(' ')]+' ...'
		print '<'+data
		self.connection.send(data+'\r\n')
		
	# PRIVMSG
	def message(self, to, msg):
		for line in msg.split('\n'):
			line = line.replace('\r','')
			self.send('PRIVMSG '+to+' :'+line)
			time.sleep(self.delay)

	# NOTICE
	def notice(self, to, msg):
		for line in msg.split('\n'):
			line = line.replace('\r','')
			self.send('NOTICE '+to+' :'+line)
#			time.sleep(self.delay)
	
	def join(self, channel):
		self.send('JOIN '+channel+'\r\n')

	def part(self, channel, reason):
		self.send('PART '+channel+' :'+reason+'\r\n')

	def auth(self):
		self.message('NickServ', 'IDENTIFY '+raw_input('NickSerk password: ')+'\r\nSET AUTOOP ON')

	def addGod(self, nick):
		if nick not in self.gods:
			self.gods.append(nick.replace(',', ''))
			
	def removeGod(self, nick):
		if nick in self.gods:
			self.gods.remove(nick.replace(',', ''))
			
	def isGod(self, nick):
		return nick in self.gods
		
	def getGods(self):
		return ', '.join(self.gods)

	def godMessage(self, message):
		for god in self.gods:
			self.message(god, message)
			
	def setDelay(self, time):
		self.delay = time
	
	def getDelay(self):
		return self.delay
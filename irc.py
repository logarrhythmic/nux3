#!/usr/bin/python
# -*- coding: UTF-8 -*-

import inspect_shell
import socket
import time
import sys

class irc:
	def __init__(self, network, serverport, localport):
		self.network = network
		self.serverport = serverport
		self.localport = localport
		self.gods = []
		self.authenticated = False
		
		# connect to IRC
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((network, serverport))
		
	def recv(self):
		data = self.irc.recv(self.localport).strip('\n\r')
		if not self.authenticated and data.find('MOTD') != -1:
			self.authenticated = True
			self.auth()
		return data

	def send(self, data):
		data = data.split('\n')[0]
		if len(data) > 496:
			data = data[:data[:500].rfind(' ')]+' ...'
		print '<'+data
		self.irc.send(data+'\r\n')
		
	# PRIVMSG
	def message(self, to, msg):
		for line in msg.split('\n'):
			line = line.replace('\r','')
			self.send('PRIVMSG '+to+' :'+line)
			time.sleep(0.5)
	
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
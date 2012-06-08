#!/usr/bin/python
# -*- coding: UTF-8 -*-

import inspect_shell
import socket
import time
import sys
	
def recv(irc):
	data = irc.recv(self.localport).strip('\n\r')
	# NickServ authentication
	if not authenticated and data.find('MOTD') != -1:
		authenticated = True
		irc.auth(irc)
	return data

def send(irc, data):
	data = data.split('\n')[0]
	if len(data) > 396:
		data = data[:data[:400].rfind(' ')]+' ...'
	print '<'+data
	self.irc.send(data+'\r\n')
	
# PRIVMSG
def message(irc, to, msg):
	for line in msg.split('\n'):
		line = line.replace('\r','')
		self.send('PRIVMSG '+to+' :'+line)
		time.sleep(self.delay)

# NOTICE
def notice(irc, to, msg):
	for line in msg.split('\n'):
		line = line.replace('\r','')
		irc.send('NOTICE '+to+' :'+line)
		time.sleep(self.delay)

def join(irc, channel):
	irc.send('JOIN '+channel+'\r\n')

def part(irc, channel, reason):
	irc.send('PART '+channel+' :'+reason+'\r\n')

def auth(irc):
	irc.message('NickServ', 'IDENTIFY '+raw_input('NickSerk password: ')+'\r\nSET AUTOOP ON')

def addGod(gods, nick):
	if nick not in gods:
		irc.gods.append(nick.replace(',', ''))
	return gods
		
def removeGod(gods, nick):
	if nick in gods:
		gods.remove(nick.replace(',', ''))
	return gods	
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
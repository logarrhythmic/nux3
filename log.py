#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

class Set:
	def __init__(self):
		self.channels = []
	
	def addChannel(self, name):
		for channel in self.channels:
			if channel.getName() == name:
				return
		self.channels.append(Channel(name))
	
	def removeChannel(self, name):
		for channel in self.channels:
			if channel.getName() == name:
				self.channels.remove(Channel(name))

	def addMessage(self, name, nick, message):
		for channel in self.channels:
			if channel.getName() == name:
				channel.addMessage(nick, message)
	
	def getMessage(self, name, quote):
		for channel in self.channels:
			if channel.getName() == name:
				return channel.getMessage(quote)

class Channel:
	def __init__(self, name):
		self.name = name
		self.messages = []
		self.nicks = []
		
	def addMessage(self, nick, message):
		if len(self.nicks) >= 10:
			self.nicks = self.nicks[1:]
			self.messages = self.messages[1:]
		self.nicks.append(nick)
		self.messages.append(message)
			
	def getMessage(self, quote):
		for nick, line in zip(reversed(self.nicks), reversed(self.messages)):
			if re.match(quote, line):
				return nick+' '+line
		return ''
		
	def getName(self):
		return self.name
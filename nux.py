#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import irc
#import modules

network = sys.argv[1]
serverport = 6667
god = sys.argv[2]

for arg in sys.argv:
	if arg.startswith('-n='):
		network = arg[arg.find('=')+1:]
	if arg.startswith('-p='):
		serverport = int(arg[arg.find('=')+1:])
	if arg.startswith('-g='):
		god = arg[arg.find('=')+1:]

bot = irc.Bot(network, serverport, 'nux', 'pantterin botti')
bot.addGod(god)

while 1:
	if bot.cycle():
		reload(irc)
		bot.reloadModules()
		copy = getattr(irc, 'Bot')
		bot.__class__ = copy
		print '\n*** RELOADED MODULES ***\n'
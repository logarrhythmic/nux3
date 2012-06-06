#!/usr/bin/python
# -*- coding: UTF-8 -*-

import loop
import irc
import sys

network = sys.argv[1]
serverport = 6667
localport = 4096
god = 'pantteri'

for arg in sys.argv:
	if arg.startswith('--server='):
		network = arg[arg.find('=')+1:]
	if arg.startswith('--network='):
		network = arg[arg.find('=')+1:]
	if arg.startswith('--server_port='):
		serverport = arg[arg.find('=')+1:]
	if arg.startswith('--local_port='):
		localport = arg[arg.find('=')+1:]
	if arg.startswith('--god='):
		god = arg[arg.find('=')+1:]
		

#irc = loop.loop(network, serverport, localport, god)
irc = irc.irc(network, serverport, localport)
irc.addGod(god)
irc.send('USER nux h h nux 3.0')
irc.send('NICK nux')
irc.auth()


while 1:
	if loop.cycle(irc):
		reload(loop)
		print '\n*** RELOADED MODULES ***\n'

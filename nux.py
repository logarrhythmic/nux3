#!/usr/bin/python
# -*- coding: UTF-8 -*-

import loop
import irc
import sys
import log

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
		serverport = int(arg[arg.find('=')+1:])
	if arg.startswith('--local_port='):
		localport = int(arg[arg.find('=')+1:])
	if arg.startswith('--god='):
		god = arg[arg.find('=')+1:]
		

#irc = loop.loop(network, serverport, localport, god)
connection = irc.Irc(network, serverport, localport)
connection.addGod(god)
connection.send('USER nux h h nux 3.0')
connection.send('NICK nux')
channels = log.Set()

while 1:
	if loop.cycle(connection, channels):
		reload(loop)
		print '\n*** RELOADED MODULES ***\n'

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import irc
import modules

try:
    network = sys.argv[1]
    serverport = 6667
    god = sys.argv[2]
    if len(sys.argv) > 3:
        serverport = int(sys.argv[3])

    bot = irc.Bot(network, serverport, 'nux', 'pantterin botti')
    bot.addGod(god)
    
    while 1:
        if bot.cycle():
            reload(irc)
            copy = getattr(irc, 'Bot')
            bot.__class__ = copy
            print '\n\033[37;41m*** RELOADED MODULES ***\033[0m\n'
except IndexError:
    print 'Usage: nux.py <network> <god> [<port>]'

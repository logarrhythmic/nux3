#!/usr/bin/python 
# -*- coding: UTF-8 -*-

def showhelp(bot):
    if bot.getMessage() == '!help':
        print 'dest = '+bot.getDestination()
        print 'modules: ' + str(bot.modules)
        print 'functions: ' + str(bot.functions)
        bot.message(bot.getDestination(), "kesken (ei apua)")

functions = [showhelp]
#lineCommands = {'!help': showhelp}

#!/usr/bin/python
# -*- coding: UTF-8 -*-

autoopUsers = ['apalmu', 'apouru', 'cshakes', 'ehelenius', 'jaakaappi', 'jimberg', 'jjantunen', 'jlappi', 'jtofferi', 'kivi', 'kkinnunen', 'kvoutilain', 'llaaki', 'nassikka', 'pantteri', 'ptoivanen', 'rolli', 'rraty', 'rvilppula', 'susku']

def autoop(bot):
    if bot.getCommand() == 'JOIN' and bot.getTrailing() == '#kvantit':
        user = bot.getSender()
        if user[user.find('@')+1:] == 'evo.paivola.fi' and user[user.find('!')+1:user.find('@')] in autoopUsers:
            bot.send('MODE #kvantit +o '+bot.getSenderNick())

functions = [autoop]

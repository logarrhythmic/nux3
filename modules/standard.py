#!/usr/bin/python
# -*- coding: UTF-8 -*-

def ping(bot):
    if bot.getCommand() == 'PING':
        line = bot.getLine()
        bot.send('PONG' + line[line.find(' '):])

def join(bot):
    message = bot.getMessage()
    if message.startswith('!join ') and bot.isGod(bot.getSenderNick()):
        bot.send('JOIN ' + message[message.find(' ')+1:])

def invite(bot):
    if bot.getCommand() == 'INVITE':
        channel = bot.getTrailing()
        bot.godMessage(bot.getSenderNick() + ' kutsui minut kanavalle ' + channel)
        bot.send('JOIN ' + channel)

def part(bot):
    message = bot.getMessage()
    if bot.isGod(bot.getSenderNick()):
        if message == '!part':
            bot.send('PART ' + bot.getDestination())
        if message.startswith('!part '):
            bot.send('PART ' + message[message.find(' ')+1:])

def quit(bot):
    message = bot.getMessage()
    if bot.isGod(bot.getSenderNick()) and message.startswith('!quit'):
        if message.find(' ') == -1:
            bot.send('QUIT :Killed by '+bot.getSenderNick())
        else:
            bot.send('QUIT :Killed by '+bot.getSenderNick()+' ('+message[message.find(' ')+1:]+')')
        quit()

def mode(bot):
    message = bot.getMessage()
    if bot.isGod(bot.getSenderNick()):
        if message.startswith('!mode #'):
            bot.send('MODE ' + message[message.find(' ')+1:])
        if message.startswith('!mode '):
            bot.send('MODE ' + bot.getDestination()+' '+ message[message.find(' ')+1:])

def msg(bot):
    message = bot.getMessage()
    if bot.isGod(bot.getSenderNick()) and message.startswith('!msg '):
        bot.message(message.split()[1], ' '.join(message.split()[2:]))

def quote(bot):
    message = bot.getMessage()
    if bot.isGod(bot.getSenderNick()) and message.startswith('!quote '):
        bot.send(message[7:])

def god(bot):
    message = bot.getMessage()
    if bot.isGod(bot.getSenderNick()):
        if message == '!gods':
            bot.response(', '.join(bot.getGods()))
        elif message.startswith('!god '):
            bot.addGod(message[5:])
        elif message.startswith('!devil '):
            bot.removeGod(message[7:])
        elif bot.getCommand() == 'NICK':
            bot.removeGod(bot.getSenderNick())
            bot.addGod(bot.getTrailing())
        elif bot.getCommand() == 'QUIT':
            bot.removeGod(bot.getSenderNick())

def CTCPPing(bot):
    if bot.getMessage().startswith('\001PING'):
        bot.notice(bot.getDestination(), '\001PING'+bot.getMessage()[5:])

def CTCPVersion(bot):
    if bot.getMessage().startswith('\001VERSION'):
        bot.notice(bot.getDestination(), '\001VERSION '+bot.getVersion()+'\001')

functions = [ping, CTCPPing, CTCPVersion, join, invite, part, quit, mode, msg, quote, god]
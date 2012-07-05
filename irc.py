#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import time
import sys
import traceback
import modules

def reloadCall(bot):
    if bot.isGod(bot.getSenderNick()) and bot.getMessage() == '!reload':
        bot.reload()

class Bot:
    def __init__(self, network, serverport, nickname, realname):
        self.network = network
        self.serverport = serverport
        self.gods = []
        self.authenticated = False
        self.nickname = nickname
        self.version = "nux v4.0 (beta)" 
        
        # connect to IRC
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((network, serverport))
        self.send('NICK '+nickname)
        self.send('USER '+nickname+' host irc-server :'+realname)
        self.delay = 0
        self.functions = [reloadCall]
        self.modules = modules.list
        #self.modules = ["standard", "help", "link", "dictionary", "autoop", "google"]
        for module in self.modules:
            newModule = __import__("modules."+module, fromlist = ['functions'] )
            self.functions += newModule.functions
            

    def reload(self):
        reload(modules)
        print "vanhat: "+str(self.modules)
        self.modules = modules.list
        print "uudet: "+str(self.modules)
        self.reloadModules = True 
        self.functions = [reloadCall]
        for module in self.modules:
            print sys.modules["modules."+module]
            reload(sys.modules["modules."+module])
            __import__("modules."+module)
            self.functions += sys.modules["modules."+module].functions

    def cycle(self):
        self.recv()
        self.reloadModules = False
        for function in self.functions:
            try:
                function(self)
            except:
                traceback.print_exc()
        return self.reloadModules

    def getLine(self):
        return self.line

    def getCommand(self):
        if self.line[0] == ':':
            return self.line.split()[1]
        else:
            return self.line.split()[0]

    def getSender(self):
        if self.line[0] == ':':
            return self.line.split()[0][1:]
        else:
            return ''

    def getSenderNick(self): 
        if self.line[0] == ':':
            if self.line.split()[0].find('!') != -1:
                return self.line.split()[0][1:self.line.find('!')]
            elif self.line.split()[0].find('@') != -1:
                return self.line.split()[0][1:self.line.find('@')]
            else:
                return self.line.split()[0][1:]
        else:
            return ''

    def getDestination(self):
        if self.getCommand() == 'PRIVMSG' or self.getCommand() == 'NOTICE':
            destination = self.line.split()[2]
            if destination == self.nickname:
                destination = self.getSenderNick()
            return destination
        else:
            return ''

    def getMessage(self):
        if self.getCommand() == 'PRIVMSG' or self.getCommand() == 'NOTICE':
            return self.getTrailing()
        else:
            return ''

    def getTrailing(self):
        if self.line[1:].find(':') != -1:
            return self.line[self.line[1:].find(':')+2:]
        else:
            return ''

    def getVersion(self):
        return self.version

    def response(self, message):
        self.message(self.getDestination(), message)

    def error(self, message):
        print "\033[31;1m"+message+"\033[0m"

    def recv(self):
        # receive one character at time until "\n"
        data = ""
        while 1:
            character = self.connection.recv(1)
            if character:
                # only receive one line at time
                if character == '\n':
                    break
                if character != '\r':
                    data += character
            else:
                print 'Connection closed'
                quit()
        
        print time.strftime("[%T]")+' -> '+data
        if not self.authenticated and data.find('MOTD') != -1:
            self.auth()
            self.authenticated = True
        self.line = data

    def send(self, data):
        if data.find('\n') != -1:
            data = data[:data.find('\n')]
        if len(data) > 396:
            data = data[:data[:400].rfind(' ')]+' ...'
        print time.strftime("[%T]")+' <- '+data
        self.connection.send(data+'\r\n')
        
    # PRIVMSG
    def message(self, to, msg):
        for line in msg.split('\n'):
            line = line.replace('\r','')
            self.send('PRIVMSG '+to+' :'+line)
            time.sleep(self.delay)

    # NOTICE
    def notice(self, to, msg):
        for line in msg.split('\n'):
            line = line.replace('\r','')
            self.send('NOTICE '+to+' :'+line)
#            time.sleep(self.delay)
    
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
        return self.gods

    def godMessage(self, message):
        for god in self.gods:
            self.message(god, message)
            
    def setDelay(self, time):
        self.delay = time
    
    def getDelay(self):
        return self.delay

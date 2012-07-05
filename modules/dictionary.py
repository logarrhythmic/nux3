#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import http

def urbanDictionary(bot):
    message = bot.getMessage()
    if message.startswith('!ud '):
        definition = 'Ei tuloksia'
        data = http.gethttp('http://www.urbandictionary.com/define.php?term='+urllib2.quote(message[4:])).split('\n')
        for line in data:
            if line.find('class="definition"') != -1:
                definition = http.cleanHTML(line)
                break
        try:
            bot.response(http.parseHTML(definition))
        except:
            bot.error('PROBLEM WHILE UNESCAPING HTML')
            bot.response(definition)

def dictionaryDotCom(bot):
    message = bot.getMessage()
    if message.startswith('!define '):
        word = message[8:]
        site = http.gethttp('http://dictionary.reference.com/browse/'+urllib2.quote(word))

        if site.find('<span class="nr">') == -1:
            if site.find('<div class="pbk">') == -1:
                bot.error('<div class="pbk"> NOT FOUND')
                bot.error('word = "'+word+'"')
                return
            else:
                exp = site.split('<div class="pbk">')[1]
                if exp.find('<div class="dndata">') != -1:
                    exp = exp.split('<div class="dndata">')[1]
                elif exp.find('<div class="luna-Ent">') != -1:
                    exp = exp.split('<div class="luna-Ent">')[1]
                else:
                    bot.error('word = "'+word+'"')
                    bot.response('error')
                    return
            exp = exp[:exp.find('</div>')]
            print word+' - '+http.cleanHTML(exp)
            bot.response(word+' - '+http.cleanHTML(exp))
        else:
            site = site[site.find('<span class="nr">')+17:]
            site = site[:site.find('</span>')]
            print word+site
            bot.response(word+site)

functions = [urbanDictionary, dictionaryDotCom]

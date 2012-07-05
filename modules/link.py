#!/usr/bin/python
# -*- coding: UTF-8 -*-

import http
import time

def title(bot):
    message = bot.getMessage()
    if message.find('://') != -1:
        for link in message.split():
            if link.find('http://') != -1 or link.find('https://') != -1:
                realurl = http.geturl(link)
                print realurl+' '
                if realurl.find('://www.youtube.com/watch') != -1:
                    data = http.gethttp(realurl)
                    bot.response(youtube(data))
                else:
                    data = http.gethttp(realurl)
                    if data.find('<title>') != -1 and data.find('</title>') != -1:
                        title = data[data.find('<title>')+7:]
                        title = title[:title.find('</title>')]
                        print 'Title: '+title
                        bot.response('Title: '+http.cleanHTML(title)+' (at '+hilightHost(realurl)+')')
                    else:
                        bot.response('No title (at '+hilightHost(realurl)+')')
                        
def hilightHost(url):
    hostStart = url.find('://')+3
    hostEnd = url[hostStart:].find('/')+hostStart
    return url[:hostStart]+'\002'+url[hostStart:hostEnd]+'\002'+url[hostEnd:]

def youtube(data):
    title = data[data.find('<meta name="title" content="')+28:]
    title = http.cleanHTML(title[:title.find('">')])

    duration = data[data.find('<meta itemprop="duration" content="PT')+37:]
    duration = http.cleanHTML(duration[:duration.find('">')])
    minutes = duration[:duration.find('M')]
    seconds = duration[duration.find('M')+1:duration.find('S')]
    if int(minutes) > 59:
        hours = int(minutes)/60
        if int(minutes)%60 < 10:
            minutes = str(hours)+':0'+str(int(minutes)%60)
        else:
            minutes = str(hours)+':'+str(int(minutes)%60)
    if int(seconds) < 10:
        seconds = '0'+seconds

    return '[Youtube] \002'+title+'\002 ('+minutes+':'+seconds+')'

functions = [title]
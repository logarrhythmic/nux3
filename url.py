import urllib2

	# Urban Dictionary
	if cmd == '!ud':
		conn = httplib.HTTPConnection("www.urbandictionary.com")
		conn.request("GET", "/define.php?term=" + urllib.quote_plus(arg))
		r1 = conn.getresponse()
		data = r1.read().split("\n")
		conn.close()
		answer = "ei tuloksia"
		for line in data:
			if line.find('class="definition"') != -1:
				answer = h.unescape(re.sub(r'<[^>]*>','',line))
				break
		message(sender, answer)

	# What's special in today
	if cmd == '!day':
		date = time.strftime('%B_%-d')
		conn = httplib.HTTPConnection("en.wikipedia.org")
		conn.request("GET", "/wiki/"+date)
		r1 = conn.getresponse()
		data = r1.read().split("\n")
		conn.close()
		fun = []
		add = False
		for line in data:
			if add:
				if line.find(' Births') != -1:
					break
				else:
					fun.append(re.sub(r'<[^>]*>','',line))
			if line.find(' Events') != -1:
				add = True
		message(sender, time.strftime('%-d.%-m.') + random.choice(fun[1:-1]))
		
	# Wolfram|Alpha
	if cmd == '!wa':
		result = "ei tuloksia"
		conn = httplib.HTTPConnection("www.wolframalpha.com")
		conn.request("GET", "/input/?i=" + urllib.quote_plus(arg))
		r1 = conn.getresponse()
		wa = r1.read().split('\n')
		conn.close()
		n = 0
		for line in wa:
			if line.find('stringified') != -1:
				n+=1
				if(n == 2):
					result = line.split('"')[ 3 ].replace("\\n","\r\n")
		# todo: make a nice array
		message(sender, result)
		
	# Maze
	if cmd == '!maze':
		print '"'+arg+'"'
		try:
			x = int(arg[:arg.find('x')])
			print x
			y = int(arg[arg.find('x')+1:])
			print y
			if y > 30 or x > 100:
				message(sender, 'suurin koko on 100x30')
			elif x < 3 or y < 3:
				message(sender, 'pienin koko on 3x3')
			else:
				maze = os.popen('java Generator '+str(x)+' '+str(y)+' | ./box.sh').read()
				if nick == god or y < 6:
					message(sender, maze)
				else:
					message(nick, maze)
		except ValueError:
			message(sender, 'syntaksi: !maze <leveys>x<korkeus>')
		except IndexError:
			message(sender, 'syntaksi: !maze <leveys>x<korkeus>')
					
print '\n############\n'.join(urllib2.urlopen('http://data.stackexchange.com/users/7095'))
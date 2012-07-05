def calc(expression):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Nux/3.1')]
		google = ''.join(opener.open('http://www.google.com/search?q='+
			urllib2.quote(expression)))
		print google
		if google.find('<h2 class="r" dir="ltr"') != -1:
			answer = google[google.find('class="r" dir="ltr"'):]
			answer = answer[answer.find('>')+1:answer.find('<')]
			return unescape('\00300[\00312G\00304o\00308o\00312g\00309l\00304e\00300] \003\002'
			+answer)
		else:
			return unescape('\00300[\00312G\00304o\00308o\00312g\00309l\00304e\00300] \002'
			+'\00304Could not calculate!')


	except Exception as e:
		print 'EXCEPTION WITH CALCULATION "'+expression+'"'
		print e
		return unescape('\00300[\00312G\00304o\00308o\00312g\00309l\00304e\00300] '
		+'\00304COULD NOT CALCULATE')

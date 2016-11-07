import psycopg2
import bmbuffer
import BMStream
def parse(funclist,socket,**kwargs):
	try:
		socket.send(bytes('rating system connected. Type (exclamation)rating to see your rating, (exclamation)balance to see the balance of teams, (exclamation)topten to see the top ten players, (exclamation)coyote to hear a coyote\n'))
		bms = kwargs['bms']
		while (True):
			bms.read()
			while bms.isEmpty():
				bmdict = bms.pop()
				for bmfunc in funclist:
					bmfunc(bmdict,socket,**kwargs)
	except KeyboardInterrupt:
		print "exiting"
		socket.send('rating system disconnected\n')
		socket.close()
		kwargs.get('dbcursor').close()
		
		
		

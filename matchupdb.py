from datetime import datetime
from databaseaccesslayer import find_player,add_player, matchupdate, most_recent_steam, apply_elo
def read_and_write(string,comparator,bmstream, socket):
	while True:
		print string
		socket.send(bytes(string))
		bmstream.read()
		try:	
			print bmstream.isEmpty()
			while bmstream.isEmpty():
				bmdict = bmstream.pop()
				if bmdict['option'] == comparator:
					return bmdict
				else: 
					print bmdict
		except KeyboardInterrupt:
			print "was in read and write phase"
def is_running(packet, socket, **kwargs):
	if packet['option'] == 'Chat':
		if "coyote" in packet['content']:
			conn = kwargs['dbcursor']
			bmstream = kwargs['bms']

			socket.send(bytes("awoooooo!\n"))

def matchupdb(packet, socket, **kwargs):
	if packet['option'] == 'Killfeed':		
		conn = kwargs['dbcursor']
		bmstream = kwargs['bms']

		cur = conn.cursor()
		dt = datetime.now()

		socket.send(bytes('/steam '+packet['victim']+'\n'))
		bmstream.read()
		victimdict = bmstream.pop()

		socket.send(bytes('/steam '+packet['killer']+'\n'))
		bmstream.read()
		killerdict = bmstream.pop()
		try:
			victimid = find_player(victimdict['player'], victimdict['steamid'], cur)
		except KeyError:
			print "packet accessed was not a player"
			print victimdict
			return
		if victimid is None:
			
			print "has no steamid"
			print victimdict['steamid'] == '-1'
			if victimdict['steamid'] == '-1':
				victimid = add_player(victimdict['player'], victimdict['steamid'],dt,cur)[0]
				print "adding " + victimid['player'] + victimdict['steamid'] + str(victimid)
			else:
				player_id = most_recent_steam(victimdict['steamid'], cur)
				
				print  "his steam"+str(player_id)
				print "victim's id " + str(player_id)
				if not player_id:	#player has steam profile and is first time on server
					victimid = add_player(victimdict['player'], victimdict['steamid'], dt, cur)[0]
				else:	#player has steam profile and isn't first time on server
					print "not the first time on server"
					victimid = add_player(victimdict['player'], victimdict['steamid'], dt, cur, player_rating(player_id, cur))
		try:
			killerid = find_player(killerdict['player'], killerdict['steamid'], cur)
		except KeyError:
			print killerdict
			print "packet accessed was not player"
			return
		if not killerid:
			if killerdict['steamid'] == -1:
				killerid = add_player(killerdict['player'], killerdict['steamid'],dt,cur)[0]
			else:
				player_id = most_recent_steam(killerdict['steamid'], cur)
				print "killers id " + str(player_id)
				if not player_id:	#player has steam profile and is first time on server
					killerid = add_player(killerdict['player'], killerdict['steamid'], dt, cur)[0]
				else:	#player has steam profile and isn't first time on server
					killerid = add_player(killerdict['player'], killerdict['steamid'], dt, cur, player_rating(player_id, cur))
	

		newrating = apply_elo(victimid, killerid, cur)
		matchupdate(newrating[0],newrating[1], 
			victimdict['player'], killerdict['player'],
			victimid, killerid,
			packet['cause'], cur)
		conn.commit()


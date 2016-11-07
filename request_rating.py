from matchupdb import most_recent_steam
from databaseaccesslayer import player_rating
import re
#Displays the player's rating when !rating is typed into chat
def request_rating(packet, socket, **kwargs):
	if (packet['option'] == 'Chat'):
		if "!rating" in packet['content']:

			conn = kwargs['dbcursor']
			bmstream = kwargs['bms']
			cur = conn.cursor()
			socket.send('/steam '+packet['name'] +'\n')
			bmstream.read()
			playerdict = bmstream.pop()
			if playerdict['option'] != "Steam ID":
				return 
			print playerdict
			if playerdict['steamid'] == -1:
				cur.execute("""
					SELECT rating FROM player
					WHERE ingamename = (%s);""",
					(re.split(': ',packet['content'])[0],))
				rating = cur.fetchone()[0]
			else:
				playerid = most_recent_steam( playerdict['steamid'], cur)
				rating = player_rating(playerid, cur)
			if rating:
				print rating
				socket.send(bytes(packet['name'] + ': ' + str(rating) + '\n'))

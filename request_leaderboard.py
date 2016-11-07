
def top_player(cur):
	cur.execute("""SELECT ingamename,rating
				FROM player
				ORDER BY rating DESC LIMIT 10;""")
	return cur.fetchall()

def request_leaderboard(packet,socket, **kwargs):
	if packet['option'] == "Chat":
		if "!topten" in packet['content']:
			conn = kwargs['dbcursor']
			bmstream = kwargs['bms']

			leaderboard = str(top_player(conn.cursor()))
			socket.send(leaderboard+'\n')
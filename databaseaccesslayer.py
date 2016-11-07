from datetime import datetime
#takes a name and a steamid and returns a player_id 
def find_player(name, steamid, cur):
	cur.execute(
		"""SELECT player_id FROM player 
		WHERE ingamename = (%s) AND steamid = (%s);""",
		(name, str(steamid))
	)
	return cur.fetchone()

#returns the rating given a playerid
def player_rating(playerid, cur):
	cur.execute(
		"""SELECT rating FROM player 
		WHERE player_id = (%s);""",
		(playerid,)
	)
	try:
		rating = cur.fetchone()[0]
		return rating
	except TypeError:
		return 1000
#adds a player to the player database table
def add_player(name, steamid,date,cur,rating = 1000):
	cur.execute(
		"""INSERT INTO player (ingamename, steamid, rating, datecreated)
			VALUES(%s, %s, %s, %s);""",
		(name, steamid, rating, date)
		)
	return find_player(name, str(steamid), cur)

#given two ids, uses the elo function to adjust ratings
def apply_elo(victimid, killerid, cur):
	victim_rating = player_rating(victimid, cur)
	print "victim " + str(victim_rating)
	
	killer_rating = player_rating(killerid, cur)
	print "killer" + str(killer_rating)
	victimnewrating = elo(victim_rating, killer_rating)[0]
	killernewrating = elo(victim_rating, killer_rating)[1]

	cur.execute(
		"""
		UPDATE player SET rating = (%s)
		WHERE player_id = (%s);""",
		(victimnewrating, victimid))
	cur.execute(
		"""
		UPDATE player SET rating = (%s)
		WHERE player_id = (%s);""",
		(killernewrating, killerid))
	return [victimnewrating, killernewrating]

#inserts a new matchup entry in the matchup table
def matchupdate(victimrating, killerrating, victimname, killername, victimid, killerid, weaponused, cur):
	cur.execute(
		"""INSERT INTO matchup (weapon, victimrating, killerrating,victim_name, killer_name, victim_id, killer_id,dateoccurred)
			VALUES(%s, %s, %s, %s,%s, %s, %s, %s);""",
		(weaponused, victimrating, killerrating, victimname, killername, victimid, killerid, datetime.now())
	)


#function that gets the latest steam given a steamid
def most_recent_steam(steamid, cur):
	if steamid != -1: #not an anonymous player
		cur.execute(
			"""SELECT player_id 
			FROM player 
			WHERE steamid = (%s)
			ORDER BY datecreated DESC LIMIT 1;""",
			((str(steamid),)))
		return cur.fetchone()
		
#Elo rating adjustment
def elo(victimrating,killerrating):
	r1 = 10**(float(victimrating)/400)
	r2 = 10**(float(killerrating)/400)
	e1 = r1 / (r1 + r2)
	e2 = r2 / (r1 + r2)
	print e1
	print e2
	r1 = victimrating - 32*e1
	r2 = killerrating + 32*(1 - e2)
	return [r1,r2]

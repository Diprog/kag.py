class PlayerActions():
	"""
		0: logged into client or ("opened game")
		1: joined server
		2: playing on server
		3: left server
	"""
	LOGGED_IN = 0
	JOINED_SERVER = 1
	PLAYING_SERVER = 2
	LEFT_SERVER = 3

class PlayerRoles():
	"""
		0: Normal player account
		1: KAG dev/team member
		2: KAG Guard
		3: Unsure, only test accounts seem to have this. Probably should be treated as KAG staff (subject to change)
		4: KAG team member ("admin" level, more or less the same as type 1)
		5: KAG tester
	"""
	USER = 0
	SUPER = 1
	POLICE = 2
	MOD = 3
	ADMIN = 4
	TESTER = 5

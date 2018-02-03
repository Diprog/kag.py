import json as _json
import kag


class KAGObject:
	def __str__(self):
		return _json.dumps(self.json)
	def __repr__(self):
		return str(self.json)

class ServerStatus(KAGObject):
	def __init__(self, json):
		self.json = json
		self.dn_cycle = json.get("DNCycle")
		self.dn_state = json.get("DNState")
		self.ipv4_address = json.get("IPv4Address")
		self.ipv6_address = json.get("IPv6Address")
		self.build = json.get("build")
		self.build_type = json.get("buildType")
		self.connectable = json.get("connectable")
		self.current_players = json.get("currentPlayers")
		self.description = json.get("description")
		self.first_seen = json.get("firstSeen")
		self.game_id = json.get("gameID")
		self.game_mode = json.get("gameMode")
		self.game_state = json.get("gameState")
		self.gold = json.get("gold")
		self.internal_ipv4 = json.get("internalIPv4")
		self.last_update = json.get("lastUpdate")
		self.map_h = json.get("mapH")
		self.map_name = json.get("mapName")
		self.map_w = json.get("mapW")
		self.max_players = json.get("maxPlayers")
		self.max_spectator_players = json.get("maxSpectatorPlayers")
		self.mod_name = json.get("modName")
		self.mods_verified = json.get("modsVerified")
		self.name = json.get("name")
		self.num_bots = json.get("numBots")
		self.password = json.get("password")
		self.player_list = json.get("playerList")
		self.player_percentage = json.get("playerPercentage")
		self.port = json.get("port")
		self.prefer_af = json.get("preferAF")
		self.reserved_players = json.get("reservedPlayers")
		self.spectator_players = json.get("spectatorPlayers")
		self.sub_game_mode = json.get("usingMods")
		self.using_mods = json.get("playerList")
		self.version = json.get("version")

	def get_ip_port(self):
		return f"{self.ipv4_address}:{self.port}"

	def get_minimap_url(self):
 		return kag.get_server_minimap_url(self.ipv4_address, self.port)
		
class Server(KAGObject):
	def __init__(self, json):
		self.json = json
		self.server_ipv4_address = json.get("serverIPv4Address")
		self.server_ipv6_address = json.get("serverIPv6Address")
		self.server_port = json.get("serverPort")

	def get_status(self):
		return kag.get_server_status(self.server_ipv4_address, self.server_port)

	def get_ip_port(self):
		return f"{self.server_ipv4_address}:{self.server_port}"

	def get_minimap_url(self):
		return kag.get_server_minimap_url(self.server_ipv4_address, self.server_port)

class PlayerStatus(KAGObject):
	def __init__(self, json):
		self.json = json
		self.found = False if json.get("statusMessage") else True
		self.action = json.get("action")
		self.last_update = json.get("lastUpdate")
		self.server = Server(json["server"]) if json.get("server") else None

class PlayerInfo(KAGObject):
	def __init__(self, json):
		self.json = json
		self.active = json.get("active")
		self.ban_expiration = json.get("banExpiration")
		self.ban_reason = json.get("banReason")
		self.banned = json.get("banned")
		self.gold = json.get("gold")
		self.gold_storm = json.get("gold_storm")
		self.gold_trenchrun = json.get("gold_trenchrun")
		self.rating = json.get("rating")
		self.reg_unix_time = json.get("regUnixTime")
		self.registered = json.get("registered")
		self.role = json.get("role")
		self.username = json.get("username")

class Player(KAGObject):
	def __init__(self, json):
		self.json = json
		self.info = PlayerInfo(json["playerInfo"])
		self.status = PlayerStatus(json["playerStatus"])
		self.ban_flags = PlayerBanFlags(json["playerBanFlags"])

class PlayerInfoPrivate(PlayerInfo):
	def __init__(self, json):
		PlayerInfo.__init__(self, json)
		self.receive_emails = json.get("receiveEmails")
		self.terms_accepted = json.get("termsAccepted")

class PlayerInfoForum(PlayerInfo):
	def __init__(self, json):
		PlayerInfo.__init__(self, json)
		self.email = json.get("email")
		self.user_id = json.get("user_id")

class PlayerBanFlags(KAGObject):
	def __init__(self, json):
		self.json = json
		self.all = json.get("all")
		self.current = json.get("current")

class PlayerAvatar(KAGObject):
	def __init__(self, json):
		self.json = json
		self.large = json.get("large")
		self.medium = json.get("medium")
		self.small = json.get("small")

import requests
import base64
from kag.errors import *
from kag.objects import *

endpoint = "https://api.kag2d.com/v1"

def http_basic_base64_auth(username, password):
	form = "%s:%s" % (username, password)
	base64_auth_info = base64.standard_b64encode(bytes(form, "utf8"))
	headers = {"Authorization":"Basic " + base64_auth_info.decode("utf8")}
	return headers

def get(path, params={}, headers={}):
	print(endpoint + path)
	response = requests.get(endpoint + path, params=params, headers=headers)
	status_code = response.status_code
	#print(status_code)
	#print(response.headers)
	json = response.json()
	if (status_code == 200):
		return json
	elif (status_code == 401):
		raise InvalidAuth(status_code, "Invalid username or password", json)
	elif (status_code == 403):
		raise UsernameMismatch(status_code, "Username in the header does not match the username in the URL, or the player is inactive", json)
	elif (status_code == 404):
		if (json.get("statusMessage")):
			raise StatusNotFound(status_code, "Player status not found, or player is banned", json)
		else:
			raise PlayerNotFound(status_code, "Could not find a player by given username", json)

def get_player(username):
	json = get(f"/player/{username}")
	return Player(json)

def get_player_info(username):
	json = get(f"/player/{username}/info")
	return PlayerInfo(json["playerInfo"])

def get_player_status(username):
	json = get(f"/player/{username}/status")
	return PlayerStatus(json["playerStatus"])

def get_player_myinfo(username, password):
	headers = http_basic_base64_auth(username, password)
	json = get(f"/player/{username}/myinfo", headers)
	return PlayerInfoPrivate(json)

def get_player_foruminfo(username, password):
	headers = http_basic_base64_auth(username, password)
	json = get(f"/player/{username}/foruminfo", headers)
	return PlayerInfoForum(json)

def get_player_banflags(username):
	json = get(f"/player/{username}/banflags")
	return PlayerBanFlags(json)

def get_player_avatar(username, size=None):
	path = f"/player/{username}/avatar"
	if (size):
		path += "/" + size
	json = get(path)
	return json[list(json.keys())[0]] if size else PlayerAvatar(json)

def get_server_status(ip, port):
	json = get(f"/game/thd/kag/server/{ip}/{port}/status")
	return ServerStatus(json["serverStatus"])

def get_server_minimap_url(ip, port):
	return f"/game/thd/kag/server/{ip}/{port}/minimap"

def get_servers(limit=10, start=0):
	params = {"limit":limit, "start":start}
	json = get("/game/thd/kag/servers", params)
	servers = json["serverList"]
	for i, server in enumerate(servers):
		servers[i] = ServerStatus(server)
	return servers

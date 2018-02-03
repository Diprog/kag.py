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
	"""
	Use this method to get player information, player status and player ban flags.

	Args:
		username (:obj:`str`): username of a KAG player.

	Returns:
		:class:`kag.objects.Player`
	"""
	json = get(f"/player/{username}")
	return Player(json)

def get_player_info(username):
	"""
	Use this method to get only player information.

	Args:
		username (:obj:`str`): username of a KAG player.

	Returns:
		:class:`kag.objects.PlayerInfo`
	"""
	json = get(f"/player/{username}/info")
	return PlayerInfo(json["playerInfo"])

def get_player_status(username):
	"""
	Use this method to get only player status.

	Args:
		username (:obj:`str`): username of a KAG player.

	Returns:
		:class:`kag.objects.PlayerStatus`
	"""
	json = get(f"/player/{username}/status")
	return PlayerStatus(json["playerStatus"])

def get_player_myinfo(username, password):
	"""
	Use this method to get player's private info. Same as :obj:`kag.get_player_info`, but returns two more fileds: `receive_emails` and `terms_accepted`.

	Args:
		username (:obj:`str`): username of a KAG account.
		password (:obj:`str`): password of a KAG account.

	Returns:
		:class:`kag.objects.PlayerInfoPrivate`
	"""
	headers = http_basic_base64_auth(username, password)
	json = get(f"/player/{username}/myinfo", headers)
	return PlayerInfoPrivate(json)

def get_player_foruminfo(username, password):
	"""
	Use this method to get player's private forum info. Same as :obj:`kag.get_player_info`, but returns two more fileds: `email` and `user_id`.

	Args:
		username (:obj:`str`): username of a KAG account.
		password (:obj:`str`): password of a KAG account.

	Returns:
		:class:`kag.objects.PlayerInfoForum`
	"""
	headers = http_basic_base64_auth(username, password)
	json = get(f"/player/{username}/foruminfo", headers)
	return PlayerInfoForum(json)

def get_player_banflags(username):
	"""
	Use this method to get player's ban flags.

	Args:
		username (:obj:`str`): username of a KAG account.

	Returns:
		:class:`kag.objects.PlayerBanFlags`
	"""
	json = get(f"/player/{username}/banflags")
	return PlayerBanFlags(json)

def get_player_avatar(username, size=None):
	"""
	Use this method to get player's avatar urls.

	Args:
		username (:obj:`str`): username of a KAG account.
		size (:obj:`str`, optional): pass only ``l`` (large), ``m`` (medium) or ``s`` (small).

	Returns:
		:obj:`str`: if size is specified, :class:`kag.objects.PlayerAvatar` otherwise.
	"""
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

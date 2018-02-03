from functools import wraps

class KAGError(Exception):
	def __init__(self, status_code, message, json):
		self.status_code = status_code
		self.json = json
	def __str__(self):
		return "%s - %s" % (self.status_code, self.message)
	def __repr__(self):
		return self.__str__()

class PlayerNotFound(KAGError):
	pass

class StatusNotFound(KAGError):
	pass

class InvalidAuth(KAGError):
	pass

class UsernameMismatch(KAGError):
	pass

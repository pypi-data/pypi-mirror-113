from .objects import *


class Hypixel:

	def __init__(self, api):
		if api = "DEV":
			self.api = "d44a57f7-ebe1-4b05-9370-9db9c94d9464"
		else:
			self.api = api

		self.player = get_player(self.api)
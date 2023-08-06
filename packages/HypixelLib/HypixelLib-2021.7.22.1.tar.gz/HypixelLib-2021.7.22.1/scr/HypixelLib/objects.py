import requests
import asyncio
import json

from .exceptions import APIError, NoInputError
from .utils import key_check
from .Mojang import get_uuid
from .hypixelplayer import Player

HYPIXEL_API = "https://api.hypixel.net"


class get_player:

	def __init__(self, api):
		self.api = api


	def get(self, name=None, uuid=None):

		if name == None and uuid == None:
			raise NoInputError

		if not name == None:
			uuid = get_uuid(name)
		response = requests.get(f"{HYPIXEL_API}/player?key=d44a57f7-ebe1-4b05-9370-9db9c94d9464&uuid={uuid}")
		json = response.json()

		if not json["success"]:

			raise APIError(self.api)
		else:
			return Player(json)
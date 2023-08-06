import requests
import asyncio
import json

from .exceptions import APIError, NoInputError
from .utils import key_check
from .Mojang import get_uuid


HYPIXEL_API = "https://api.hypixel.net"


class Player:

	def __init__(self, data):

		self.name = data.get("player", {}).get("displayname")
		self.uuid = data.get("player", {}).get("uuid")
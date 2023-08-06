import requests

HYPIXEL_API = "https://api.hypixel.net"

def key_check(api):
	response = request.get(f"{HYPIXEL_API}/key?key={api}")
	json = response.json()
	if not json["success"]:
		raise InvalidAPIKeyError(api)
	return APIKey
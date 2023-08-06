from ..utils import Games



class Bedwars:

	def __init__(self, data):
		self.name = "Bedwars"
		self.solo = Solo(data)
		self.games = Games(
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("games_played_bedwars"),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("wins_bedwars"),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("losses_bedwars")
			)
		self.beds = Beds(
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("beds_broken_bedwars"),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("beds_lost_bedwars")
			)


#Returns the broken/destroyed Beds
class Beds:
	def __init__(self, broken, lost):
		self.name = "Beds destroyed/broken"
		self.destroyed = broken
		self.lost = lost


#Bedwars Solo rounds
class Solo:

	def __init__(self, data):

		self.name = "Solo"
		self.games = Games(
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_games_played_bedwars", 0),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_wins_bedwars", 0),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_losses_bedwars", 0),
			)

		self.beds = Beds(
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eigth_one_beds_broken_bedwars", 0),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_beds_lost_bedwars", 0)
			) 
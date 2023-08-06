from ..utils import Games



class Bedwars:

	def __init__(self, data):
		self.name = "Bedwars"
		self.coins = data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("coins", 0)
		self.solo = Solo(data)
		
		#Games
		self.games = Games(
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("games_played_bedwars"),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("wins_bedwars"),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("losses_bedwars")
			)
		
		#Beds
		self.beds = Beds(
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("beds_broken_bedwars"),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("beds_lost_bedwars")
			)
		
		#Kills/deaths
		self.kills = data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("kills_bedwars", 0)
		self.final_kills = data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_kills_bedwars", 0)
		self.deaths = data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("deaths_bedwars", 0)
		self.final_deaths = data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_deaths_bedwars", 0)
		
		#Items
		self.items = Items(data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("items_pruchased_bedwars"), 0)

		#Resources
		self.resources = Resources(
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("resources_collected_bedwars", 0),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("iron_resources_collected_bedwars", 0),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("gold_resources_collected_bedwars", 0),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("diamond_resources_collected_bedwars", 0),
			data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("emerald_resources_collected_bedwars", 0)
			)


class Items:

	def __init__(self, items_purchased):

		self.purchased = items_purchased
		


class Resources:

	def __init__(self, _all, iron, gold, diamond, emeralds):
		
		self.all = _all
		self.iron = iron
		self.gold = gold
		self.diamonds = diamonds
		self.emeralds = emeralds

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
		self.kills = data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_kills_bedwars", 0)
		self.final_kills = data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_final_kills_bedwars", 0)
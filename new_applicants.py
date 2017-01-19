# New applicants arrive into your project database by this script.
# You can run it anytime to generate new data!

from models import *
import random

names = [
		"Tomi", "Anna", "Zotya", "Tibi", 
		"Jani", "Sanyi", "Orsi", "Kitti", 
		"Ond", "Kond", "Tas", "Huba", 
		"Töhötöm", "Álmos", "Előd"
		]

cities = ["Debrecen", "Szeged", "Budapest", "Warsaw", "Székesfehérvár"]

def generate_applicant():
	random_name = random.choice(names)
	random_city = random.choice(cities)
	names.remove(random_name)
	Applicant.create(name=random_name,status='new',city=random_city)
	print("\nNew applicant --{}-- created\n".format(random_name))	
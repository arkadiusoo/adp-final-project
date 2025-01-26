import pandas as pd
import json

# 1. Wczytaj dane z folderu data
rent_data = pd.read_csv('data/apartments_rent_pl_2023_11.csv')

job_offers = json.load(open('data/justjoinit-2023-09-25.json'))

# 2. Wyfiltruj dane dla miast: Warsaw, Katowice, Wroclaw, Krakow
cities = ["warszawa", "warsaw", "katowice", "wrocław",
          "wroclaw", "kraków", "krakow"]

filtered_rent_data = rent_data[rent_data['city'].str.lower().isin(cities)]

filtered_job_offers = []

for offer in job_offers:
    if offer.get('city', '').lower() in cities:
        filtered_job_offers.append(offer)

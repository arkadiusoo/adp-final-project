import pandas as pd
import json
import geopandas as gpd
from shapely.geometry import Point

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

# Przekonwertuj dane na GeoDataFrame oraz przeprowadź projekcję CRS na EPSG:4326
rent_gdf = gpd.GeoDataFrame(
    filtered_rent_data,
    geometry=gpd.points_from_xy(filtered_rent_data['longitude'],
                                filtered_rent_data['latitude']),
    crs='EPSG:4326'
)
job_gdf = gpd.GeoDataFrame(
    filtered_job_offers,
    geometry=[Point(offer['longitude'], offer['latitude'])
              for offer in filtered_job_offers],
    crs="EPSG:4326"
)


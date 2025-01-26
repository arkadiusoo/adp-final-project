import pandas as pd
import json
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import MarkerCluster

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

# 3. Przekonwertuj dane na GeoDataFrame oraz przeprowadź projekcję CRS na EPSG:4326
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
# 4. Utwórz mapę wycentrowaną na centrum Warszawy
map_center = [52.2297, 21.0122]
base_map = folium.Map(location=map_center, zoom_start=6, tiles="CartoDB Positron")

# 5. Utwórz wartstwy
rent_markers = MarkerCluster(name="Mieszkania").add_to(base_map)

for _, row in rent_gdf.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=(
            f"<b>Miasto:</b> {row['city']}<br>"
            f"<b>Cena:</b> {row['price']} PLN<br>"
            f"<b>Metraż:</b> {row['squareMeters']} m²"
        ),
        icon=folium.Icon(color="blue", icon="home", prefix="fa"),
    ).add_to(rent_markers)

job_markers = MarkerCluster(name="Oferty pracy").add_to(base_map)

for _, row in job_gdf.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=(
            f"<b>Miasto:</b> {row['city']}<br>"
            f"<b>Stanowisko:</b> {row['title']}<br>"
            # f"<b>Wynagrodzenie:</b> {row['salary']}"
        ),
        icon=folium.Icon(color="green", icon="briefcase", prefix="fa"),
    ).add_to(job_markers)

folium.LayerControl(collapsed=False).add_to(base_map)
base_map.save('rent_map.html')
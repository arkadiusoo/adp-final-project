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

# 3. Przekonwertuj dane na GeoDataFrame
# oraz przeprowadź projekcję CRS na EPSG:4326
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

# 4. Wygeneruj mapy dla każdego miasta z ofetami pracy oraz mieszkań
city_coordinates = {
    "Warszawa": [52.2297, 21.0122],
    "Katowice": [50.2599, 19.0216],
    "Wrocław": [51.1079, 17.0385],
    "Kraków": [50.0647, 19.9450],
}


# Funkcja do generowania mapy dla danego miasta
def generate_city_map(city_name, city_coords, rent_gdf, job_gdf):
    city_map = folium.Map(location=city_coords, zoom_start=12,
                          tiles="CartoDB Positron")

    rent_markers = MarkerCluster(name="Mieszkania").add_to(city_map)
    for _, row in rent_gdf[
        rent_gdf['city'].str.lower() == city_name.lower()].iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=(
                f"<b>Miasto:</b> {row['city']}<br>"
                f"<b>Cena:</b> {row['price']} PLN<br>"
                f"<b>Metraż:</b> {row['squareMeters']} m²"
            ),
            icon=folium.Icon(color="blue", icon="home", prefix="fa"),
        ).add_to(rent_markers)

    # Grupa znaczników dla ofert pracy
    job_markers = MarkerCluster(name="Oferty pracy").add_to(city_map)
    for _, row in job_gdf[
        job_gdf['city'].str.lower() == city_name.lower()].iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=(
                f"<b>Miasto:</b> {row['city']}<br>"
                f"<b>Stanowisko:</b> {row['title']}<br>"
            ),
            icon=folium.Icon(color="green", icon="briefcase", prefix="fa"),
        ).add_to(job_markers)

    folium.LayerControl(collapsed=False).add_to(city_map)

    file_name = "output/{}_map.html".format(city_name.lower())
    city_map.save(file_name)
    return file_name


# Generowanie map dla każdego miasta
map_files = []
for city_name, city_coords in city_coordinates.items():
    map_file = generate_city_map(city_name, city_coords, rent_gdf, job_gdf)
    map_files.append((city_name, map_file))
print(len(map_files))
# Tworzenie strony HTML z czterema mapami
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Mapy Miast</title>
    <style>
        .map-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
        }}
        iframe {{
            width: 100%;
            height: 500px;
            border: none;
        }}
    </style>
</head>
<body>
    <h1>Mapy Miast: Warszawa, Wroclaw, Krakow, Katowice</h1>
    <div class="map-container">
        {map_iframes}
    </div>
</body>
</html>
"""

# Tworzenie iframe dla każdej mapy
map_iframes = ""
for city_name, map_file in map_files:
    map_iframes += f'<iframe src="{map_file}" title="Mapa: {city_name}"></iframe>\n'

# Wypełnienie szablonu iframe'ami
final_html = html_content.format(map_iframes=map_iframes)


with open("miasta_mapy.html", "w", encoding="utf-8") as f:
    f.write(final_html)

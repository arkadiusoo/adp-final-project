import pandas as pd
import json
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic
import html_template as htm

# 1. Wczytaj dane z folderu data
rent_data = pd.read_csv('../data/apartments_rent_pl_2023_11.csv')

job_offers = json.load(open('../data/justjoinit-2023-09-25.json'))

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
    "Wroclaw": [51.1079, 17.0385],
    "Karkow": [50.0647, 19.9450],
}


# Funkcja do filtrowania danych na podstawie odległości
# od współrzędnych miasta
def filter_data_within_city(data_gdf, city_coords, radius_km=10):
    filtered_data = []
    for _, row in data_gdf.iterrows():
        point_coords = (row.geometry.y, row.geometry.x)
        if geodesic(point_coords, city_coords).km <= radius_km:
            filtered_data.append(row)
    return filtered_data


# Funkcja do generowania mapy dla danego miasta
def generate_city_map(city_name, city_coords, rent_gdf,
                      job_gdf, radius_km=10):
    city_map = folium.Map(location=city_coords,
                          zoom_start=12, tiles="CartoDB Positron")

    # Filtruj mieszkania w obrębie miasta
    rent_filtered = filter_data_within_city(rent_gdf, city_coords, radius_km)
    rent_markers = MarkerCluster(name="Mieszkania").add_to(city_map)
    for row in rent_filtered:
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=(
                f"<b>Miasto:</b> {city_name}<br>"
                f"<b>Cena:</b> {row['price']} PLN<br>"
                f"<b>Metraż:</b> {row['squareMeters']} m²"
            ),
            icon=folium.Icon(color="blue", icon="home", prefix="fa"),
        ).add_to(rent_markers)

    # Filtruj oferty pracy w obrębie miasta
    job_filtered = filter_data_within_city(job_gdf, city_coords, radius_km)
    job_markers = MarkerCluster(name="Oferty pracy").add_to(city_map)
    for row in job_filtered:
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=(
                f"<b>Miasto:</b> {city_name}<br>"
                f"<b>Stanowisko:</b> {row['title']}<br>"
            ),
            icon=folium.Icon(color="green", icon="briefcase", prefix="fa"),
        ).add_to(job_markers)

    folium.LayerControl(collapsed=False).add_to(city_map)

    file_name = f"../output/{city_name.lower()}_map.html"
    city_map.save(file_name)
    return file_name


# Generowanie map dla każdego miasta
map_files = []
for city_name, city_coords in city_coordinates.items():
    map_file = generate_city_map(city_name, city_coords,
                                 rent_gdf, job_gdf, radius_km=10)
    map_files.append((city_name, map_file))
# Tworzenie poprawionego HTML
html_content = htm.html_content

# Tworzenie sekcji dla każdej mapy
map_sections = ""
for city_name, map_file in map_files:
    map_sections += f"""
    <div class="city-map">
        <h2>{city_name}</h2>
        <iframe src="{map_file}" title="Mapa: {city_name}"></iframe>
    </div>
    """

# Wypełnienie szablonu sekcjami map
final_html = html_content.format(map_sections=map_sections)

# Zapis do pliku HTML
with open("../output/miasta_mapy.html", "w", encoding="utf-8") as f:
    f.write(final_html)

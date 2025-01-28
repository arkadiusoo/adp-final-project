import json
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import transform
import pyproj
import contextily as ctx
import matplotlib.pyplot as plt

job_offers = json.load(open('../data/justjoinit-2023-09-25.json'))

filtered_job_offers = []

cities = ["warszawa", "warsaw", "katowice", "wrocław",
          "wroclaw", "kraków", "krakow"]

for offer in job_offers:
    if offer.get('city', '').lower() in cities:
        filtered_job_offers.append(offer)

job_gdf = gpd.GeoDataFrame(
    filtered_job_offers,
    geometry=[Point(offer['longitude'], offer['latitude'])
              for offer in filtered_job_offers],
    crs="EPSG:4326"
)

city_coordinates = {
    "Warszawa": [52.2297, 21.0122],
    "Katowice": [50.2599, 19.0216],
    "Wrocław": [51.1079, 17.0385],
    "Kraków": [50.0647, 19.9450],
}

selected_columns = ['city', 'title', 'latitude', 'longitude', 'employment_type', 'avg_salary', 'currency', 'salaryForMap']

# Tworzenie DataFrame
df = pd.DataFrame(columns=selected_columns)
for index, row in job_gdf.iterrows():
    if row['employment_types'][0]['salary'] is not None:
        avg_salary = row['employment_types'][0]['salary']['to'] - row['employment_types'][0]['salary']['from'] / 2
        if row['employment_types'][0]['salary']['currency'] == 'usd':
            avg_salary_map = round(avg_salary * 4.03)
        elif row['employment_types'][0]['salary']['currency'] == 'eur':
            avg_salary_map = round(avg_salary * 4.2)
        else:
            avg_salary_map = avg_salary
        df.loc[len(df)] = [row['city'], row['title'], row['latitude'], row['longitude'], row['employment_types'][0]['type'], avg_salary, row['employment_types'][0]['salary']['currency'], avg_salary_map]

# Tworzenie GeoDataFrame
df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
new_job_gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
new_job_gdf = new_job_gdf.to_crs(epsg=3857)

# Tworzenie bufora (20 km) wokół miast
def city_point(city_coords):
    return Point(city_coords[1], city_coords[0])

city_buffers = {
    city_name: transform(
        pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform,
        city_point(city_coords)
    ).buffer(10000)  # Bufor 20 km w EPSG:3857
    for city_name, city_coords in city_coordinates.items()
}

# Filtrowanie punktów w promieniu 20 km od miast
filtered_data = []
for _, row in new_job_gdf.iterrows():
    point = row.geometry
    for city_name, buffer in city_buffers.items():
        if buffer.contains(point):  # Sprawdzanie, czy punkt jest w buforze
            filtered_data.append(row)
            break  # Jeśli pasuje do jednego miasta, nie musimy sprawdzać dalej

# Tworzenie nowego GeoDataFrame z przefiltrowanych danych
filtered_gdf = gpd.GeoDataFrame(filtered_data, crs="EPSG:3857")

# Tworzenie kategorii wynagrodzeń
filtered_gdf['salary_range'] = pd.qcut(filtered_gdf['salaryForMap'], 5)
filtered_gdf['salary_range_label'] = pd.qcut(
    filtered_gdf['salaryForMap'], q=5,
    labels=[f"{int(interval.left)} - {int(interval.right)} PLN" for interval in filtered_gdf['salary_range'].cat.categories]
)

# Wizualizacja map
fig, axs = plt.subplots(2, 2, figsize=(14, 14))
axs = axs.flatten()

for i, (city_name, city_coords) in enumerate(city_coordinates.items()):
    city_data = filtered_gdf[filtered_gdf['city'].str.lower() == city_name.lower()]

    city_data.plot(
        column='salary_range_label',
        cmap='RdYlBu',
        linewidth=0,
        ax=axs[i],
        legend=False
    )

    ctx.add_basemap(
        axs[i],
        crs=city_data.crs.to_string(),
        source=ctx.providers.OpenStreetMap.Mapnik,
    )

    axs[i].set_title(f"{city_name}: Rozkład płac", fontsize=14)
    axs[i].set_axis_off()

    unique_categories = sorted(
        city_data['salary_range_label'].unique(),
        key=lambda x: int(x.split(' ')[0]),
        reverse=True
    )

    colors = plt.cm.RdYlBu(np.linspace(0, 1, len(unique_categories)))

    legend_patches = [
        mpatches.Patch(color=colors[i], label=str(cat)) for i, cat in enumerate(unique_categories)
    ]

    axs[i].legend(handles=legend_patches, title="Zakres cen (PLN)", loc='upper right', fontsize=10, title_fontsize=12)

plt.tight_layout()
plt.show()

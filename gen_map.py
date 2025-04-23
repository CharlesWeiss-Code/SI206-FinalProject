import folium
import folium.plugins
from datetime import datetime, timedelta
import csv_manipulation
import os
import json
import math
import sqlite3

skip_value = int(input("Enter the skip value: "))
threshold = 0.1

# Establish SQLite connection and create table
conn = sqlite3.connect("covid_data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS time_series_data (
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    intensity FLOAT NOT NULL,
    date TEXT NOT NULL
)
""")

# Process data as in the original script
data = csv_manipulation.get_time_series_dict(csv_manipulation.read_csv(), skip_value=skip_value)

clipped_data = [
    [[point[0], point[1], max(0, point[2])] for point in time_step]
    for time_step in data
]

transformed_data = [
    [[point[0], point[1], math.log1p(point[2])] for point in time_step]
    for time_step in clipped_data
]

global_max_transformed = max(
    max(point[2] for point in time_step)
    for time_step in transformed_data if any(point[2] > 0 for point in time_step)
) or 1  # Avoid division by zero

normalized_data = [
    [[point[0], point[1], point[2] / global_max_transformed] for point in time_step]
    for time_step in transformed_data
]

# Generate time index
start_date = datetime(year=2020, month=1, day=22)
time_index = [
    (start_date + k * timedelta(days=skip_value)).strftime("%Y-%m-%d") for k in range(len(normalized_data))
]

# Clear existing data and insert normalized_data into the database
cur.execute("DELETE FROM time_series_data")
for day, time_step in enumerate(normalized_data):
    date = time_index[day]
    for point in time_step:
        cur.execute(
            "INSERT INTO time_series_data (lat, lon, intensity, date) VALUES (?, ?, ?, ?)",
            (point[0], point[1], point[2], date)
        )
conn.commit()

# Retrieve time_index and curated_data from the database
cur.execute("SELECT DISTINCT date FROM time_series_data ORDER BY date")
time_index = [row[0] for row in cur.fetchall()]

curated_data = []
for date in time_index:
    cur.execute("""
        SELECT lat, lon,
               CASE WHEN intensity > ? THEN intensity ELSE 0 END AS intensity
        FROM time_series_data
        WHERE date = ?
    """, (threshold, date))
    day_data = cur.fetchall()
    curated_data.append([[row[0], row[1], row[2]] for row in day_data])

conn.close()

# Create Folium map (unchanged from original)
m = folium.Map([39.8333, -98.5833], zoom_start=4, max_zoom=10, min_zoom=4)

gradient = {
    "0.0": "transparent",
    "0.1": "blue",
    "0.3": "cyan",
    "0.5": "lime",
    "0.7": "yellow",
    "1.0": "red"
}

hm = folium.plugins.HeatMapWithTime(
    curated_data,
    index=time_index,
    auto_play=True,
    max_opacity=0.8,
    gradient=gradient,
    radius=15,
    overlay=True,
    name="Covid-19 Heatmap"
)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
).add_to(m)

geojson_path = "./data/us-states.json"
with open(geojson_path, 'r') as f:
    state_borders = json.load(f)

folium.GeoJson(
    state_borders,
    name="State Borders",
    style_function=lambda x: {
        "color": "white",
        "weight": 1,
        "opacity": 0.5,
        "fillOpacity": 0
    },
).add_to(m)

hm.add_to(m)

title_html = '''
    <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 9999;
                background-color: rgba(255, 255, 255, 0.5); padding: 5px 10px; border-radius: 5px;">
        <h3 style="margin: 0; font-size: 20px;"><b>COVID-19 Confirmed Cases Heatmap (2020)</b></h3>
    </div>
'''
m.get_root().html.add_child(folium.Element(title_html))

temp_file_path = "heatmap_with_time.html"
m.save(temp_file_path)

safari_path = "open -a Safari"
full_command = f"{safari_path} {temp_file_path}"
os.system(full_command)
import folium
import folium.plugins
from datetime import datetime, timedelta
import csv_manipulation
import os
import json

skip_value = 20

data = csv_manipulation.get_time_series_dict(csv_manipulation.read_csv(), skip_value=skip_value)

# print(data)

start_date = datetime(year=2020,month=1,day=22)

time_index = [
    (start_date + k * timedelta(1)*skip_value).strftime("%Y-%m-%d") for k in range(len(data))
]
m = folium.Map([39.8333, -98.5833], zoom_start=4,max_zoom=7,min_zoom=4)

hm = folium.plugins.HeatMapWithTime(data,index=time_index,auto_play=True,max_opacity=0.5, name="Covid-19 Heatmap",blur=1)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
).add_to(m)

geojson_path = "./data/us-states.json"  # Adjust the path to your GeoJSON file
with open(geojson_path, 'r') as f:
    state_borders = json.load(f)

# Add the state borders to the map
folium.GeoJson(
    state_borders,
    name="State Borders",
    style_function=lambda x: {
        "color": "white",  # Border color
        "weight": 1,  # Border thickness
        "opacity": 0.5,  # Border opacity
        "fillOpacity": 0  # No fill, just the borders
    },
).add_to(m)

hm.add_to(m)

# Save the map to an HTML file
temp_file_path = "heatmap_with_time.html"
m.save(temp_file_path)

# Open the HTML file in Safari
safari_path = "open -a Safari"  # Command to open with Safari on macOS
full_command = f"{safari_path} {temp_file_path}"
os.system(full_command)
import folium
import folium.plugins
from datetime import datetime, timedelta
import csv_manipulation
import os
import json
import math

skip_value = 20

data = csv_manipulation.get_time_series_dict(csv_manipulation.read_csv(), skip_value=skip_value)

sigmoid_intensities = [1 / (1 + math.exp(-i)) for i in data]

# print(data)

start_date = datetime(year=2020,month=1,day=22)

time_index = [
    (start_date + k * timedelta(1)*skip_value).strftime("%Y-%m-%d") for k in range(len(data))
]
# m = folium.Map([39.8333, -98.5833], zoom_start=4,max_zoom=6,min_zoom=4)
m = folium.Map([39.8333, -98.5833], zoom_start=4, max_zoom = 10, min_zoom = 4)


gradient = {
    "0.1": "blue",
    "0.3": "cyan",
    "0.5": "lime",
    "0.7": "yellow",
    "1.0": "red"
}

hm = folium.plugins.HeatMapWithTime(data,
    index=time_index,
    auto_play=True,
    max_opacity=0.8,  # Increase for better visibility
    gradient=gradient,  # Prettier colors
    radius=25,
    overlay=True,
    # scale_radius=True,
    name="Covid-19 Heatmap")

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

title_html = '''
    <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 9999; 
                background-color: rgba(255, 255, 255, 0.8); padding: 5px 10px; border-radius: 5px;">
        <h3 style="margin: 0; font-size: 20px;"><b>COVID-19 Confirmed Cases Heatmap (2020)</b></h3>
    </div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map to an HTML file
temp_file_path = "heatmap_with_time.html"
m.save(temp_file_path)

# Open the HTML file in Safari
safari_path = "open -a Safari"  # Command to open with Safari on macOS
full_command = f"{safari_path} {temp_file_path}"
os.system(full_command)
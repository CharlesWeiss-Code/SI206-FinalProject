import folium
import folium.plugins
from datetime import datetime, timedelta
import csv_manipulation
import os
import json

skip_value = 20

# Assuming csv_manipulation.get_time_series_dict processes your data correctly
data = csv_manipulation.get_time_series_dict(csv_manipulation.read_csv(), skip_value=skip_value)

start_date = datetime(year=2020, month=1, day=22)
time_index = [
    (start_date + k * timedelta(1) * skip_value).strftime("%Y-%m-%d") for k in range(len(data))
]

# Create the map with a satellite tile layer for a prettier background
m = folium.Map(
    location=[39.8333, -98.5833],  # Center of contiguous US
    zoom_start=4,
    max_zoom=7,
    min_zoom=4,
    tiles="Esri.WorldImagery",  # High-quality satellite imagery
    attr="Esri"
)

# Define a vibrant gradient for the heatmap
gradient = {
    "0.1": "blue",
    "0.3": "cyan",
    "0.5": "lime",
    "0.7": "yellow",
    "1.0": "red"
}

# Add the heatmap with enhanced visual parameters
hm = folium.plugins.HeatMapWithTime(
    data,
    index=time_index,
    auto_play=True,
    max_opacity=0.8,  # Increase for better visibility
    radius=30,        # Slightly larger for smoothness
    blur=15,          # Softer blending
    gradient=gradient,  # Prettier colors
    name="Covid-19 Heatmap"
)
hm.add_to(m)

# Load the GeoJSON file for state borders
geojson_path = "./data/us-states.json"
with open(geojson_path, 'r') as f:
    state_borders = json.load(f)

# Add state borders with improved styling
folium.GeoJson(
    state_borders,
    name="State Borders",
    style_function=lambda x: {
        "color": "white",  # Visible against satellite imagery
        "weight": 2,       # Thicker borders
        "opacity": 0.8,    # Slightly transparent
        "fillOpacity": 0   # No fill to focus on heatmap
    }
).add_to(m)

# Add a simple, elegant title
title_html = '''
    <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 9999;
                background-color: rgba(255, 255, 255, 0.8); padding: 5px 10px; border-radius: 5px;">
        <h3 style="margin: 0;">COVID-19 Confirmed Cases Heatmap (2020)</h3>
    </div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map to an HTML file
temp_file_path = "prettier_heatmap.html"
m.save(temp_file_path)

# Open the HTML file in Safari
safari_path = "open -a Safari"  # Adjust if not on macOS
full_command = f"{safari_path} {temp_file_path}"
os.system(full_command)
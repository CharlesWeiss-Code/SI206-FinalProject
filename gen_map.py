import folium
import folium.plugins
import numpy as np
from datetime import datetime, timedelta
import webbrowser
import os

# Data
np.random.seed(3141592)
initial_data = np.random.normal(size=(100, 2)) * np.array([[1, 1]]) + np.array(
    [[48, 5]]
)

move_data = np.random.normal(size=(100, 2)) * 0.01

data = [(initial_data + move_data * i).tolist() for i in range(100)]

# Weights
time_ = 0
N = len(data)
itensify_factor = 30
for time_entry in data:
    time_ = time_+1
    for row in time_entry:
        weight = min(np.random.uniform()*(time_/(N))*itensify_factor, 1)
        row.append(weight)

# Time Index
time_index = [
    (datetime.now() + k * timedelta(1)).strftime("%Y-%m-%d") for k in range(len(data))
]

# Map
m = folium.Map([48.0, 5.0], zoom_start=6)

hm = folium.plugins.HeatMapWithTime(data, index=time_index, auto_play=True, max_opacity=0.3)

hm.add_to(m)

# Save the map to an HTML file
temp_file_path = "heatmap_with_time.html"
m.save(temp_file_path)

# Open the HTML file in Safari
safari_path = "open -a Safari"  # Command to open with Safari on macOS
full_command = f"{safari_path} {temp_file_path}"
os.system(full_command)
import folium
import folium.plugins
from datetime import datetime, timedelta
import csv_manipulation
import os

data = csv_manipulation.get_time_series_dict(csv_manipulation.read_csv(), skip_value=100)

# print(data)

start_date = datetime(year=2020,month=1,day=22)

time_index = [
    (start_date + k * timedelta(1)).strftime("%Y-%m-%d") for k in range(len(data))
]
m = folium.Map([44.9672,-98.50], zoom_start=6)

hm = folium.plugins.HeatMapWithTime(data,index=time_index,auto_play=True,max_opacity=0.3)

hm.add_to(m)

# Save the map to an HTML file
temp_file_path = "heatmap_with_time.html"
m.save(temp_file_path)

# Open the HTML file in Safari
safari_path = "open -a Safari"  # Command to open with Safari on macOS
full_command = f"{safari_path} {temp_file_path}"
os.system(full_command)
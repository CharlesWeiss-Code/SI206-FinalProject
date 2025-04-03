import folium
import webbrowser
import os
from folium.plugins import HeatMap
from folium.plugins import LayerControl

MAP_PATH = "us_satellite_map.html"
BORDERS_PATH = "data/us-states.json"

def generate_map():
    us_center = [39.8283, -98.5795]
    bounds = [[24.396308, -125.0], [49.384358, -66.93457]]

    m = folium.Map(
        location=us_center,
        zoom_start=4,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        maxBounds=bounds,
        maxZoom=10,
        minZoom=3,
        maxBoundsViscosity=0.0
    )

    with open(BORDERS_PATH, 'r') as f:
        state_borders = f.read()
    folium.GeoJson(
        state_borders,
        name="State Borders",
        style_function=lambda x: {'fillColor': 'transparent', 'color': 'white', 'weight': 1, 'opacity': 0.3}
    ).add_to(m)

    folium.Marker(
        location=[40.71088124, -73.81684712],
        popup="Test Marker",
        icon=folium.Icon(color="red")
    ).add_to(m)

    heatmap_data = [
        [[40.71, -73.81, 100], [34.05, -118.24, 70]],
        [[40.71, -73.81, 100], [34.05, -118.24, 70], [38.90, -77.03, 50]],
        [[40.71, -73.81, 100], [34.05, -118.24, 70], [38.90, -77.03, 50], [42.36, -71.05, 80]]
    ]
    time_indices = ["2020-01-01", "2020-01-02", "2020-01-03"]

    for i, frame in enumerate(heatmap_data):
        HeatMap(
            data=frame,
            name=time_indices[i],
            radius=15,
            blur=10,
            gradient={'0.4': 'blue', '0.65': 'yellow', '1': 'red'}
        ).add_to(m)

    LayerControl().add_to(m)

    m.save(MAP_PATH)

def open_map():
    html_path = os.path.abspath(MAP_PATH)
    webbrowser.get("chrome").open(f"file://{html_path}")

def main():
    generate_map()
    open_map()

if __name__ == "__main__":
    main()
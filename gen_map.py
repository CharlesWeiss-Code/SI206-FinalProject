from csv_manipulation import *
import folium
import webbrowser
import os

MAP_PATH = "us_satellite_map.html"
BORDERS_PATH = "data/us-states.json"


def generate_map():
    us_center = [39.8283, -98.5795]  # Approximate center of the contiguous US

    # Define the bounds to limit the zoom to US and Canada
    bounds = [[24.396308, -125.0], [49.384358, -66.93457]]  # Southwest and Northeast corners for US

    # Create a map with satellite tiles
    m = folium.Map(
        location=us_center,
        zoom_start=4,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        maxBounds=bounds,  # Restrict panning within these bounds
        maxZoom=10,  # Limit the maximum zoom level
        minZoom=3,  # Allow more zoom-out level for a broader view
        maxBoundsViscosity=0.0
    )

    # Load state borders from the local file you downloaded
    with open(BORDERS_PATH, 'r') as f:
        state_borders = f.read()

    # Add the GeoJSON for state borders
    folium.GeoJson(
        state_borders,
        name="State Borders",
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'white',
            'weight': 1,
            'opacity':0.3
        }
    ).add_to(m)

    # Save the map to an HTML file
    m.save(MAP_PATH)

def open_map():
    html_path = os.path.abspath(MAP_PATH)
    webbrowser.get("safari").open(f"file://{html_path}")

def main():
    generate_map()
    open_map()

if __name__ == "__main__":
    main()

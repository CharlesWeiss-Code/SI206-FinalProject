import sqlite3
import csv_manipulation
from datetime import datetime, timedelta

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



# cur.execute("""DROP TABLE IF EXISTS time_series_data""")
skip_value = 2

cur.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name=?;
""", ("time_series_data",))
res = cur.fetchone() is not None

if res:
    date = datetime(year=2020,month=1,day=22)
    time_series_data = csv_manipulation.get_time_series_dict(csv_manipulation.read_csv(), skip_value=skip_value)
    for time_step in time_series_data:

        for point in time_step:
            if point[0] == 0 or point[1] == 0:
                continue
            cur.execute("""
            INSERT INTO time_series_data (lon, lat, intensity, date) VALUES (?, ?, ?, ?)
            """, (point[0], point[1], point[2], date.strftime("%Y-%m-%d")))
        date += timedelta(1) * skip_value    

print(res)
conn.commit()
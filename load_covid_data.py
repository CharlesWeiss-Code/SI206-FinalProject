import requests
import sqlite3
from datetime import datetime

#connecting to SQL database
conn = sqlite3.connect("covid_data.db")
cur = conn.cursor()

#creating a state_metadata table
cur.execute("""
CREATE TABLE IF NOT EXISTS state_metadata (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_abbr TEXT UNIQUE
)
""")

#adding the state abbreviations
states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
]
for abbr in states:
    cur.execute("INSERT OR IGNORE INTO state_metadata (state_abbr) VALUES (?)", (abbr,))

#creating a covid_data table
cur.execute("""
CREATE TABLE IF NOT EXISTS covid_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    state TEXT,
    state_id INTEGER,
    death INTEGER,
    hospitalizedCurrently INTEGER,
    positiveIncrease INTEGER,
    UNIQUE(date, state)
)
""")

#getting the COVID data from API #1
url = "https://api.covidtracking.com/v1/states/daily.json"
response = requests.get(url)
data = response.json()

count = 0
for row in data:
    raw_date = row.get("date")
    state = row.get("state")
    if not state or not raw_date:
        continue

    #this is the current format like 20210307
    #I am converting it date to YYYY-MM-DD format so the two tables can
    #share an interger key
    try:
        date = datetime.strptime(str(raw_date), "%Y%m%d").strftime("%Y-%m-%d")
    except:
        continue

    #getting the state_id from state_metadata
    cur.execute("SELECT state_id FROM state_metadata WHERE state_abbr = ?", (state,))
    match = cur.fetchone()
    if not match:
        continue
    state_id = match[0]

    #making sure to skip duplicates to avoid errors
    cur.execute("SELECT 1 FROM covid_data WHERE date = ? AND state = ?", (date, state))
    if cur.fetchone():
        continue

    cur.execute("""
        INSERT OR IGNORE INTO covid_data (
            date, state, state_id, death, hospitalizedCurrently, positiveIncrease
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date, state, state_id,
        row.get("death"), row.get("hospitalizedCurrently"), row.get("positiveIncrease")
    ))

    count += 1
    if count >= 25:
        break
#makings sure i am adding 25 at a time, and so I can see that I am actually adding this data in
print(f"{count} new COVID rows inserted.")

#creating a vaccination_data table
cur.execute("""
CREATE TABLE IF NOT EXISTS vaccination_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    state_id INTEGER,
    location TEXT,
    distributed INTEGER,
    administered INTEGER,
    UNIQUE(date, location)
)
""")

#getting vaccination coivd data from API #2
vacc_url = "https://data.cdc.gov/resource/unsk-b7fc.json?$limit=50000"
vacc_data = requests.get(vacc_url).json()

count = 0
for row in vacc_data:
    location = row.get("location")
    date_raw = row.get("date")
    if not location or not date_raw:
        continue

    date = datetime.strptime(date_raw.split("T")[0], "%Y-%m-%d").strftime("%Y-%m-%d")

    cur.execute("SELECT state_id FROM state_metadata WHERE state_abbr = ?", (location,))
    match = cur.fetchone()
    if not match:
        continue
    state_id = match[0]

    cur.execute("SELECT 1 FROM vaccination_data WHERE date = ? AND location = ?", (date, location))
    if cur.fetchone():
        continue

    cur.execute("""
        INSERT OR IGNORE INTO vaccination_data (
            date, state_id, location, distributed, administered
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        date, state_id, location,
        int(row.get("distributed", 0)), int(row.get("administered", 0))
    ))

    count += 1
    if count >= 25:
        break

print(f"{count} new vaccination rows inserted.")

#saving and closing
conn.commit()
conn.close()
import sqlite3
import requests

#setting up the SQL database
conn = sqlite3.connect('covid_data.db')
cur = conn.cursor()

def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Region (
        UID INTEGER PRIMARY KEY,
        iso2 TEXT,
        iso3 TEXT,
        code3 INTEGER,
        FIPS REAL,
        Admin2 TEXT,
        Province_State TEXT,
        Country_Region TEXT,
        Lat REAL,
        Long_ REAL,
        Combined_Key TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS CaseData (
        RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
        UID INTEGER,
        Date TEXT,
        Cases INTEGER,
        FOREIGN KEY (UID) REFERENCES Region (UID)
    );
    """)

create_tables()

#reading in the data from the API
def fetch_and_store_data(api_url, start=0, batch_size=25):
    response = requests.get(api_url, params={'start': start, 'limit': batch_size})
    response.raise_for_status()
    data = response.json()

    for entry in data:
        UID = entry['UID']
        iso2 = entry['iso2']
        iso3 = entry['iso3']
        code3 = entry['code3']
        FIPS = entry['FIPS']
        Admin2 = entry['Admin2']
        Province_State = entry['Province_State']
        Country_Region = entry['Country_Region']
        Lat = entry['Lat']
        Long_ = entry['Long_']
        Combined_Key = entry['Combined_Key']

        #putting this into a region tables
        cur.execute("""
        INSERT OR IGNORE INTO Region (
            UID, iso2, iso3, code3, FIPS, Admin2, Province_State, 
            Country_Region, Lat, Long_, Combined_Key
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (UID, iso2, iso3, code3, FIPS, Admin2, Province_State, Country_Region, Lat, Long_, Combined_Key))

        #making this to store the dates data
        time_series = entry['time_series']
        for date_str, cases in time_series.items():
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            cur.execute("""
            INSERT INTO CaseData (UID, Date, Cases) VALUES (?, ?, ?)
            """, (UID, date, cases))

#PUT THE API LINK HERE!
api_url = '' 
fetch_and_store_data(api_url)

conn.commit()
conn.close()

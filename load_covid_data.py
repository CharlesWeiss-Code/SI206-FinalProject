import requests
import sqlite3

# Connect to (or create) SQLite database
conn = sqlite3.connect("covid_data2.db")
cur = conn.cursor()

# Create the table if it doesn't already exist
cur.execute("""
CREATE TABLE IF NOT EXISTS covid_data2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    state TEXT,
    death INTEGER,
    deathConfirmed INTEGER,
    deathIncrease INTEGER,
    deathProbable INTEGER,
    hospitalized INTEGER,
    hospitalizedCumulative INTEGER,
    hospitalizedCurrently INTEGER,
    hospitalizedIncrease INTEGER,
    inIcuCumulative INTEGER,
    inIcuCurrently INTEGER,
    negative INTEGER,
    negativeIncrease INTEGER,
    negativeTestsAntibody INTEGER,
    negativeTestsPeopleAntibody INTEGER,
    negativeTestsViral INTEGER,
    positive INTEGER,
    positiveCasesViral INTEGER,
    positiveIncrease INTEGER,
    positiveTestsAntibody INTEGER,
    positiveTestsAntigen INTEGER,
    positiveTestsPeopleAntibody INTEGER,
    positiveTestsPeopleAntigen INTEGER,
    positiveTestsViral INTEGER,
    recovered INTEGER,
    totalTestEncountersViral INTEGER,
    totalTestEncountersViralIncrease INTEGER,
    totalTestResults INTEGER,
    totalTestResultsIncrease INTEGER,
    totalTestsAntibody INTEGER,
    totalTestsAntigen INTEGER,
    totalTestsPeopleAntibody INTEGER,
    totalTestsPeopleAntigen INTEGER,
    totalTestsPeopleViral INTEGER,
    totalTestsPeopleViralIncrease INTEGER,
    totalTestsViral INTEGER,
    totalTestsViralIncrease INTEGER,
    UNIQUE(date, state)
)
""")

# Fetch the data from the API
url = "https://api.covidtracking.com/v1/states/daily.json"
response = requests.get(url)
try:
    data = response.json()
    print("First item in data:", data[0])
except:
    print("Error parsing this JSON")
    print("Raw response text:", response.text)
    exit()

# Limit to inserting 25 new rows per run
batch_size = 25
inserted = 0

for entry in data:
    date = entry.get("date")
    state = entry.get("state")

    # Skip if this date and state already exist
    cur.execute("SELECT 1 FROM covid_data2 WHERE date = ? AND state = ?", (date, state))
    if cur.fetchone():
        continue

    values = tuple(entry.get(field, None) for field in [
        "date", "state", "death", "deathConfirmed", "deathIncrease", "deathProbable",
        "hospitalized", "hospitalizedCumulative", "hospitalizedCurrently", "hospitalizedIncrease",
        "inIcuCumulative", "inIcuCurrently", "negative", "negativeIncrease", "negativeTestsAntibody",
        "negativeTestsPeopleAntibody", "negativeTestsViral", "positive", "positiveCasesViral",
        "positiveIncrease", "positiveTestsAntibody", "positiveTestsAntigen",
        "positiveTestsPeopleAntibody", "positiveTestsPeopleAntigen", "positiveTestsViral",
        "recovered", "totalTestEncountersViral", "totalTestEncountersViralIncrease",
        "totalTestResults", "totalTestResultsIncrease", "totalTestsAntibody", "totalTestsAntigen",
        "totalTestsPeopleAntibody", "totalTestsPeopleAntigen", "totalTestsPeopleViral",
        "totalTestsPeopleViralIncrease", "totalTestsViral", "totalTestsViralIncrease"
    ])

    cur.execute("""
        INSERT OR IGNORE INTO covid_data2 (
            date, state, death, deathConfirmed, deathIncrease, deathProbable,
            hospitalized, hospitalizedCumulative, hospitalizedCurrently, hospitalizedIncrease,
            inIcuCumulative, inIcuCurrently, negative, negativeIncrease,
            negativeTestsAntibody, negativeTestsPeopleAntibody, negativeTestsViral,
            positive, positiveCasesViral, positiveIncrease,
            positiveTestsAntibody, positiveTestsAntigen, positiveTestsPeopleAntibody,
            positiveTestsPeopleAntigen, positiveTestsViral, recovered,
            totalTestEncountersViral, totalTestEncountersViralIncrease,
            totalTestResults, totalTestResultsIncrease, totalTestsAntibody,
            totalTestsAntigen, totalTestsPeopleAntibody, totalTestsPeopleAntigen,
            totalTestsPeopleViral, totalTestsPeopleViralIncrease, totalTestsViral,
            totalTestsViralIncrease
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, values)

    inserted += 1
    if inserted >= batch_size:
        break

conn.commit()
conn.close()

print(f"{inserted} new rows inserted.")

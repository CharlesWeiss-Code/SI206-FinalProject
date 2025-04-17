import sqlite3

#connecting this to the database
conn = sqlite3.connect("covid_data.db")
cur = conn.cursor()

#joining covid_data and vaccination_data on state_id and date
cur.execute("""
SELECT sm.state_abbr, 
       AVG(cd.positiveIncrease) AS avg_positive_increase, 
       AVG(vd.administered) AS avg_vaccinations
FROM covid_data cd
JOIN vaccination_data vd ON cd.state_id = vd.state_id AND cd.date = vd.date
JOIN state_metadata sm ON cd.state_id = sm.state_id
GROUP BY cd.state_id
ORDER BY sm.state_abbr
""")

results = cur.fetchall()

#writing the results into a text file
with open("average_by_state.txt", "w") as f:
    f.write("State | Avg Positive Increase | Avg Vaccinations Administered\n")
    f.write("-------------------------------------------------------------\n")
    for state, avg_pos, avg_vacc in results:
        f.write(f"{state} | {avg_pos:.2f} | {avg_vacc:.2f}\n")

print("Calculated averages written to average_by_state.txt")

#close
conn.close()


import sqlite3

#connecting to the database
conn = sqlite3.connect("covid_data2.db")
cur = conn.cursor()

# Run the query
cur.execute("""
    SELECT state, AVG(positiveIncrease) as avg_daily_cases
    FROM covid_data2
    GROUP BY state
    ORDER BY avg_daily_cases DESC
""")

results = cur.fetchall()

#saving the results to a text file like the instructions say
with open("average_positive_increase.txt", "w") as f:
    f.write("Average Daily Positive Increase per State:\n\n")
    for state, avg in results:
        f.write(f"{state}: {avg:.2f}\n")

print("Results saved to average_positive_increase.txt")

conn.close()

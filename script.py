import pandas as pd
import psycopg2 as sql
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("C:/Users/it.usnak/Desktop/policy_polrisk.csv")

# print(df.head())
# print(df.shape)
# print(df.info())
#
# df_filtered = df[df['AMOUNT'] > 500000]
#
# print(df_filtered.head())

#ploobjval

conn = sql.connect("dbname='thesoft_db' user='server_api' host='192.168.100.152' password='SunLight09+!'")

cursor  =  conn.cursor()
query = """
    SELECT policy_polrisk."POLID_F", policy_polobjval."VAL", 
           policy_polobjval."TAGID_F", policy_polrisk."RATE", 
           policy_polrisk."AMOUNT", policy_polrisk."PREMIUMS"
    FROM policy_polrisk
    INNER JOIN policy_polobjval ON policy_polrisk."POLID_F" = policy_polobjval."POLID_F"
    WHERE policy_polobjval."TAGID_F" = 372
    ORDER BY policy_polrisk."RATE" DESC
    LIMIT 100;
"""
cursor.execute(query)
results = cursor.fetchall()

years = [row[1] for row in results]
rates = [row[3] for row in results]


cursor.close()
conn.close()

sorted_years_rates = sorted(zip(years, rates))

sorted_years, sorted_rates = zip(*sorted_years_rates)

plt.figure(figsize=(10, 6))

plt.scatter(sorted_years, sorted_rates, color='b', alpha=0.7)

plt.xlabel('Year of Car Manufacturing (VAL)')
plt.ylabel('Claim Rate (RATE)')
plt.title('Claim Rate vs Year of Car Manufacturing')
plt.grid(True)

plt.show()

yearly_claims = {}
for year, rate in zip(years, rates):
    if year not in yearly_claims:
        yearly_claims[year] = []
    yearly_claims[year].append(rate)

avg_claims_by_year = {year: np.mean(rates) for year, rates in yearly_claims.items()}

sorted_years = sorted(avg_claims_by_year.keys())
avg_claims = [avg_claims_by_year[year] for year in sorted_years]

plt.figure(figsize=(10, 6))

plt.bar(sorted_years, avg_claims, color='green', alpha=0.7)

plt.xlabel('Year of Car Manufacturing (VAL)')
plt.ylabel('Average Claim Rate (RATE)')
plt.title('Average Claim Rate by Year of Car Manufacturing')
plt.grid(True)

plt.show()
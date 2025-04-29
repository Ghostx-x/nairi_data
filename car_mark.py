# import pandas as pd
# import psycopg2 as sql
# import matplotlib.pyplot as plt
# import numpy as np
#
# df = pd.read_csv("C:/Users/it.usnak/Desktop/policy_polrisk.csv")
#
# conn = sql.connect("dbname='thesoft_db' user='server_api' host='192.168.100.152' password='SunLight09+!'")
#
# cursor  =  conn.cursor()
# query = """SELECT policy_polrisk."POLID_F", policy_polobjval."VAL", policy_polobjval."TAGID_F",  policy_polrisk."RATE",  policy_polrisk."AMOUNT",  policy_polrisk."PREMIUMS"
# FROM policy_polrisk
# INNER JOIN policy_polobjval ON policy_polrisk."POLID_F" = policy_polobjval."POLID_F"
# WHERE "TAGID_F" = 386
# ORDER BY "RATE" DESC
# LIMIT 50;
# """
# cursor.execute(query)
# results = cursor.fetchall()
#
# car_mark = [row[1] for row in results]
# rates = [row[3] for row in results]
#
# cursor.close()
# conn.close()
#
# plt.figure(figsize=(10, 6))
#
# plt.bar(car_mark, rates, color='blue', alpha=0.7)
#
# plt.xlabel('Car Marks')
# plt.ylabel('Claim Rate')
# plt.title('Claim Rate vs Car Marks')
# plt.grid(True)
#
# plt.show()



import sqlite3 as sql
import matplotlib.pyplot as plt
from collections import defaultdict


conn = sql.connect("dbname='thesoft_db' user='server_api' host='192.168.100.152' password='SunLight09+!'")
cursor = conn.cursor()


query = """SELECT policy_polrisk."POLID_F", policy_polobjval."VAL", policy_polobjval."TAGID_F",  policy_polrisk."RATE",  policy_polrisk."AMOUNT",  policy_polrisk."PREMIUMS"
FROM policy_polrisk
INNER JOIN policy_polobjval ON policy_polrisk."POLID_F" = policy_polobjval."POLID_F"
WHERE "TAGID_F" = 386
ORDER BY "RATE" DESC
LIMIT 50;
"""
cursor.execute(query)
results = cursor.fetchall()


car_data = defaultdict(lambda: {'total_rate': 0, 'count': 0})


for _, car_mark, rate in results:
    car_data[car_mark]['total_rate'] += rate
    car_data[car_mark]['count'] += 1

average_rates = {mark: data['total_rate'] / data['count'] for mark, data in car_data.items()}

sorted_data = sorted(average_rates.items(), key=lambda x: x[1], reverse=True)
car_marks, avg_rates = zip(*sorted_data)

cursor.close()
conn.close()


plt.figure(figsize=(12, 6))
plt.bar(car_marks, avg_rates, color='blue', alpha=0.7)
plt.xlabel('Car Marks')
plt.ylabel('Average Claim Rate')
plt.title('Average Claim Rate vs Car Marks')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.show()
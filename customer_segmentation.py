dbname = 'thesoft_db'
user = 'server_api'
host = '192.168.100.152'
password = 'SunLight09+!'


import pandas as pd
import matplotlib.pyplot as plt
import psycopg2 as sql
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt




conn = sql.connect(dbname=dbname, user=user, host=host, password=password)
cursor = conn.cursor()

query = """
SELECT 
    EXTRACT(YEAR FROM age(c."BIRTHDAY")) AS AGE,
    COUNT(DISTINCT pol."ID") AS TOTAL_POLICIES,
    AVG(polr."PREMIUMS") AS AVG_PREMIUMS,
    AVG(polr."RATE") AS AVG_RATE
FROM 
    customer_customer c
INNER JOIN polcont_polcont pc ON c."CUSTOMER" = pc."CUSTOMER_F"
INNER JOIN policy_policy pol ON pc."CONT" = pol."CONT_F"
INNER JOIN policy_polrisk polr ON pol."ID" = polr."POLID_F"
GROUP BY AGE;

"""

cursor.execute(query)
results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(results, columns=columns)

cursor.close()
conn.close()

df = df.dropna()
df.columns = [col.upper() for col in df.columns]
df = df[df['AGE'].between(0, 70)]


import matplotlib.pyplot as plt



fig, ax1 = plt.subplots(figsize=(12, 6))


ax1.set_xlabel("Age")
ax1.set_ylabel("Average Premiums", color='tab:blue')
ax1.plot(df['AGE'], df['AVG_PREMIUMS'], color='tab:blue', label="Avg Premiums")
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel("Average Risk (Rate)", color='tab:red')
ax2.plot(df['AGE'], df['AVG_RATE'], color='tab:red', linestyle='--', label="Avg Risk")
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title("Average Premiums and Risk by Age")
fig.tight_layout()
plt.show()


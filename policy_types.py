import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import psycopg2 as sql
import numpy as np

dbname = 'thesoft_db'
user = 'server_api'
host = '192.168.100.152'
password = 'SunLight09+!'
import psycopg2 as sql
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

conn = sql.connect(dbname=dbname, user=user, host=host, password=password)
cursor = conn.cursor()

query = """
      SELECT 
        polcont_poldet."TITLE" AS "POLICY_TYPE",
        polcont_poldet."NAME_A",
        COUNT(DISTINCT policy_policy."ID") AS "POLICY_COUNT",
        SUM(policy_polrisk."PREMIUMS") AS "TOTAL_PREMIUMS",
        SUM(policy_polrisk."AMOUNT") AS "TOTAL_AMOUNT",
        SUM(policy_polrisk."PREMIUMS" - policy_polrisk."AMOUNT") AS "TOTAL_PROFIT",
        AVG((policy_polrisk."PREMIUMS" - policy_polrisk."AMOUNT") / NULLIF(policy_polrisk."PREMIUMS", 0)) AS "PROFIT_MARGIN"
    FROM 
        policy_polrisk
    INNER JOIN policy_policy ON policy_polrisk."POLID_F" = policy_policy."ID"
    INNER JOIN polcont_polcont ON policy_policy."CONT_F" = polcont_polcont."CONT"
    INNER JOIN polcont_poldet ON polcont_polcont."DETID_F" = polcont_poldet."ID"
    GROUP BY 
        polcont_poldet."TITLE", polcont_poldet."NAME_A"
    ORDER BY 
        "TOTAL_PROFIT" DESC
    LIMIT 100;
"""

cursor.execute(query)
results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(results, columns=columns)

cursor.close()
conn.close()

df["P"]
df['TOTAL_PROFIT'] = df['TOTAL_PROFIT'].astype(float)
df['PROFIT_MARGIN'] = df['PROFIT_MARGIN'].astype(float)

top_5_profit = df.nlargest(5, 'TOTAL_PROFIT')
bottom_5_profit = df.nsmallest(5, 'TOTAL_PROFIT')
df_filtered = pd.concat([top_5_profit, bottom_5_profit])


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))


bars1 = ax1.bar(df_filtered['POLICY_TYPE'], df_filtered['TOTAL_PROFIT'], color='skyblue')
ax1.set_title('Total Profit by Policy Type')
ax1.set_xlabel('Policy Type')
ax1.set_ylabel('Total Profit ($)')
ax1.tick_params(axis='x', rotation=45)

for bar in bars1:
    height = bar.get_height()
    label_y = height + 5000 if height >= 0 else height - 15000
    ax1.text(bar.get_x() + bar.get_width()/2, label_y, f'${height:,.0f}', ha='center', va='bottom' if height >= 0 else 'top')

bars2 = ax2.bar(df_filtered['POLICY_TYPE'], df_filtered['PROFIT_MARGIN'], color='lightgreen')
ax2.set_title('Profit Margin by Policy Type')
ax2.set_xlabel('Policy Type')
ax2.set_ylabel('Profit Margin')
ax2.tick_params(axis='x', rotation=45)
for bar in bars2:
    height = bar.get_height()
    label_y = height + 0.02 if height >= 0 else height - 0.05
    ax2.text(bar.get_x() + bar.get_width()/2, label_y, f'{height:.2%}', ha='center', va='bottom' if height >= 0 else 'top')


plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.3, wspace=0.3)
plt.show()

print(top_5_profit)
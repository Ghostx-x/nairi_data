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
    customer_custaddres."CUST_F", customer_custaddres."REGION", customer_custaddres."COUNTRY",
    policy_policy."OPENDATE", policy_policy."TODATE", 
    policy_polrisk."AMOUNT", policy_polrisk."RATE", policy_polrisk."PREMIUMS"
FROM 
    customer_custaddres
INNER JOIN customer_customer ON customer_custaddres."CUST_F" = customer_customer."CUSTOMER"
INNER JOIN polcont_polcont ON customer_customer."CUSTOMER" = polcont_polcont."CUSTOMER_F"
INNER JOIN policy_policy ON polcont_polcont."CONT" = policy_policy."CONT_F"
INNER JOIN policy_polrisk ON policy_policy."ID" = policy_polrisk."POLID_F"
WHERE 
    customer_custaddres."COUNTRY" = 'ARM';
"""

cursor.execute(query)
results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(results, columns=columns)

cursor.close()
conn.close()


df = df[df['REGION'] != 'NL']

df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce')
df['RATE'] = pd.to_numeric(df['RATE'], errors='coerce')
df['PREMIUMS'] = pd.to_numeric(df['PREMIUMS'], errors='coerce')
df = df[df['RATE'] >= 0] #no negative rates

df = df.dropna(subset=['REGION', 'AMOUNT', 'RATE'])



region_summary = df.groupby('REGION').agg({
    'AMOUNT': ['mean', 'sum', 'count'],
    'RATE': 'mean',
    'PREMIUMS': 'mean'
}).reset_index()

region_summary.columns = [
    'REGION',
    'avg_claim_amount', 'total_claim_amount', 'claim_count',
    'avg_claim_rate',
    'avg_premium'
]


top_amounts = region_summary.sort_values('total_claim_amount', ascending=False).head(5)
top_rates = region_summary.sort_values('avg_claim_rate', ascending=False).head(5)


print("\nTop 5 Regions by Total Claim Amount:")
print(top_amounts[['REGION', 'total_claim_amount', 'avg_claim_amount', 'claim_count']])
print("\nTop 5 Regions by Average Claim Rate:")
print(top_rates[['REGION', 'avg_claim_rate', 'claim_count']])

plt.figure(figsize=(12, 6))


plt.subplot(1, 2, 1)
sns.barplot(data=top_amounts, x='total_claim_amount', y='REGION', hue='REGION', palette='Blues_d', legend=False)
plt.title('Top 5 Regions by Total Claim Amount')
plt.xlabel('Total Claim Amount')
plt.ylabel('Region')

plt.subplot(1, 2, 2)
sns.barplot(data=top_rates, x='avg_claim_rate', y='REGION', hue='REGION', palette='Reds_d', legend=False)
plt.title('Top 5 Regions by Average Claim Rate')
plt.xlabel('Average Claim Rate')
plt.ylabel('Region')

plt.tight_layout()
plt.show()








urban_threshold = region_summary['claim_count'].quantile(0.75)
region_summary['area_type'] = region_summary['claim_count'].apply(
    lambda x: 'Urban' if x >= urban_threshold else 'Rural'
)

region_summary.to_csv('arm_claim_data.csv', index=False)
print("Exported data to 'arm_claim_data.csv'")

# Urban vs. rural summary
urban_rural_summary = region_summary.groupby('area_type').agg({
    'avg_claim_amount': 'mean',
    'avg_claim_rate': 'mean',
    'claim_count': 'sum'
}).reset_index()

print("\nUrban vs. Rural Comparison in ARM:")
print(urban_rural_summary)

# Insights and Recommendations
print("\nInsights:")
if not top_amounts.empty:
    top_region = top_amounts.iloc[0]['REGION']
    top_amount = top_amounts.iloc[0]['total_claim_amount']
    print(f"- {top_region} has the highest total claim amount ({top_amount:,.2f}).")
if not top_rates.empty:
    top_rate_region = top_rates.iloc[0]['REGION']
    top_rate = top_rates.iloc[0]['avg_claim_rate']
    print(f"- {top_rate_region} has the highest average claim rate ({top_rate:.2%}).")
if not urban_rural_summary.empty:
    urban_rate = urban_rural_summary[urban_rural_summary['area_type'] == 'Urban']['avg_claim_rate'].iloc[0]
    rural_rate = urban_rural_summary[urban_rural_summary['area_type'] == 'Rural']['avg_claim_rate'].iloc[0]
    rate_diff = (urban_rate - rural_rate) / rural_rate * 100 if rural_rate > 0 else float('inf')
    print(f"- Urban areas have {rate_diff:.1f}% higher claim rates than rural areas.")

print("\nRecommendations:")
print(f"- Adjust premiums in high-claim regions (e.g., {top_region}).")
print(f"- Increase inspections in regions with high claim rates (e.g., {top_rate_region}).")
print("- Validate urban/rural classification for ARM-specific pricing.")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2 as sql


dbname = 'thesoft_db'
user = 'server_api'
host = '192.168.100.152'
password = 'SunLight09+!'

conn = sql.connect(dbname=dbname, user=user, host=host, password=password)
cursor = conn.cursor()

debug_query = """
WITH AgeData AS (
    SELECT 
        EXTRACT(YEAR FROM age(c."BIRTHDAY")) AS AGE,
        customer_custaddres."REGION" AS "REGION",
        policy_polrisk."RATE" AS RATE
    FROM 
        customer_custaddres
    INNER JOIN customer_customer c ON customer_custaddres."CUST_F" = c."CUSTOMER"
    INNER JOIN polcont_polcont pc ON c."CUSTOMER" = pc."CUSTOMER_F"
    INNER JOIN policy_policy pol ON pc."CONT" = pol."CONT_F"
    INNER JOIN policy_polrisk ON pol."ID" = policy_polrisk."POLID_F"
    WHERE 
        customer_custaddres."COUNTRY" = 'ARM'
        AND EXTRACT(YEAR FROM c."BIRTHDAY") BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)
        AND customer_custaddres."REGION" IS NOT NULL
        AND customer_custaddres."REGION" != 'NL'
)
SELECT * FROM AgeData LIMIT 200;
"""

try:
    cursor.execute(debug_query)
    debug_results = cursor.fetchall()
    debug_columns = [desc[0] for desc in cursor.description]
    debug_df = pd.DataFrame(debug_results, columns=debug_columns)
    print("Debug: AgeData CTE Output (NL excluded):")
    print(debug_df)
except sql.Error as e:
    print(f"Debug Database error: {e}")
    raise

query = """
WITH AgeData AS (
    SELECT 
        EXTRACT(YEAR FROM age(c."BIRTHDAY")) AS AGE,
        customer_custaddres."REGION" AS "REGION",
        policy_polrisk."RATE" AS RATE
    FROM 
        customer_custaddres
    INNER JOIN customer_customer c ON customer_custaddres."CUST_F" = c."CUSTOMER"
    INNER JOIN polcont_polcont pc ON c."CUSTOMER" = pc."CUSTOMER_F"
    INNER JOIN policy_policy pol ON pc."CONT" = pol."CONT_F"
    INNER JOIN policy_polrisk ON pol."ID" = policy_polrisk."POLID_F"
    WHERE 
        customer_custaddres."COUNTRY" = 'ARM'
        AND EXTRACT(YEAR FROM c."BIRTHDAY") BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)
        AND customer_custaddres."REGION" IS NOT NULL
        AND customer_custaddres."REGION" != 'NL'
),
CustomerType AS (
    SELECT 
        "REGION",
        AGE,
        RATE,
        CASE 
            WHEN AGE BETWEEN 0 AND 25 THEN 'Young'
            WHEN AGE BETWEEN 26 AND 55 THEN 'Adult'
            WHEN AGE > 55 THEN 'Senior'
            ELSE 'Unknown'
        END AS "CUSTOMER_TYPE"
    FROM AgeData
    WHERE AGE IS NOT NULL
)
SELECT 
    "REGION",
    "CUSTOMER_TYPE",
    AVG(RATE) AS avg_claim_rate,
    COUNT(*) AS customer_count
FROM 
    CustomerType
GROUP BY 
    "REGION", "CUSTOMER_TYPE"
HAVING 
    AVG(RATE) > 0
ORDER BY 
    "REGION", avg_claim_rate DESC;
"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    if not results:
        print("Warning: No results returned from the query.")
    df = pd.DataFrame(results, columns=columns)

    if df.empty:
        print("Error: DataFrame is empty. Check the query filters or data availability.")
    elif 'REGION' not in df.columns or 'CUSTOMER_TYPE' not in df.columns:
        print(f"Error: Required columns not found in DataFrame. Available columns: {df.columns.tolist()}")
    else:

        df = df.dropna()
        df['avg_claim_rate'] = pd.to_numeric(df['avg_claim_rate'], errors='coerce')
        df = df[df['avg_claim_rate'] >= 0]


        df = df[df['CUSTOMER_TYPE'] != 'Young']


        high_risk_regions = df.groupby('REGION')['avg_claim_rate'].mean().sort_values(ascending=False).head(5).index
        df_high_risk = df[df['REGION'].isin(high_risk_regions)]


        if df_high_risk.empty:
            print("Error: No high-risk regions identified after filtering.")
        else:

            if df['avg_claim_rate'].max() > 1:
                df['avg_claim_rate'] = df['avg_claim_rate'] * 100
                df_high_risk = df_high_risk.copy()
                df_high_risk.loc[:, 'avg_claim_rate'] = df_high_risk['avg_claim_rate'] * 100
                print("Note: Converted avg_claim_rate to percentage (multiplied by 100) due to values > 1.")


            plt.figure(figsize=(12, 6))
            sns.barplot(data=df_high_risk, x='REGION', y='customer_count', hue='CUSTOMER_TYPE', palette='viridis')
            plt.title('Customer Demographics in High-Risk Regions (NL and Young Excluded)')
            plt.xlabel('Region')
            plt.ylabel('Number of Customers')
            plt.legend(title='Customer Type')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()


            print("\nDemographics in High-Risk Regions (NL and Young Excluded):")
            pivot_table = df_high_risk.pivot_table(index='REGION', columns='CUSTOMER_TYPE', values='customer_count', fill_value=0)
            print(pivot_table)

            # Insights
            print("\nInsights from High-Risk Regions (NL and Young Excluded):")
            for region in pivot_table.index:
                adult_count = pivot_table.loc[region, 'Adult'] if 'Adult' in pivot_table.columns else 0
                senior_count = pivot_table.loc[region, 'Senior'] if 'Senior' in pivot_table.columns else 0
                total = adult_count + senior_count
                adult_pct = (adult_count / total * 100) if total > 0 else 0
                senior_pct = (senior_count / total * 100) if total > 0 else 0
                print(f"- {region}: Adults ({adult_count:,}, {adult_pct:.1f}%), Seniors ({senior_count:,}, {senior_pct:.1f}%)")
            print("\nAnalysis:")
            highest_adult_region = pivot_table['Adult'].idxmax() if 'Adult' in pivot_table.columns else None
            highest_senior_region = pivot_table['Senior'].idxmax() if 'Senior' in pivot_table.columns else None
            print(f"- Region with most Adults: {highest_adult_region} ({pivot_table.loc[highest_adult_region, 'Adult'] if highest_adult_region else 0:,})")
            print(f"- Region with most Seniors: {highest_senior_region} ({pivot_table.loc[highest_senior_region, 'Senior'] if highest_senior_region else 0:,})")
            print("- YR has a significantly larger customer base, suggesting it’s a major region, but its risk profile may be diluted due to volume.")
            print("- Smaller regions like SH and LR have higher avg_claim_rates, indicating higher risk per customer.")

except sql.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    cursor.close()
    conn.close()
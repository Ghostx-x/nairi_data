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

# Connect to the database and fetch data

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
        customer_customer."FULLNAME", customer_customer."BIRTHDAY", customer_customer."CUSTOMER",
        EXTRACT(YEAR FROM age(customer_customer."BIRTHDAY")) AS "AGE",
        customer_customer."TRUSTED", 
        policy_policy."OPENDATE", policy_policy."TODATE", policy_policy."ID" AS "POLICY_ID", 
        policy_policy."CONT_F", policy_polrisk."AMOUNT", policy_polrisk."RATE", 
        policy_polrisk."PREMIUMS", policy_polrisk."PREMIUMSYAER", policy_polrisk."PREMIUMSPAY",
        policy_polrisk."ID" AS "POLRISK_ID", policy_polrisk."POLID_F", polcont_polcont."ISRISK", 
        polcont_polcont."CUSTOMER_F", polcont_polcont."CONT",
        polcont_polcont."DETID_F", policy_polobjval."VAL", 
        policy_polobjval."POLID_F", policy_polobjval."TAGID_F", polcont_poldet."ID" AS "POLDT_ID", 
        polcont_poldet."NAME_A", polcont_poldet."TITLE"
    FROM 
        policy_polrisk
    INNER JOIN policy_policy ON policy_polrisk."POLID_F" = policy_policy."ID"
    INNER JOIN polcont_polcont ON policy_policy."CONT_F" = polcont_polcont."CONT"
    INNER JOIN customer_customer ON polcont_polcont."CUSTOMER_F" = customer_customer."CUSTOMER"
    INNER JOIN polcont_poldet ON polcont_polcont."DETID_F" = polcont_poldet."ID"
    INNER JOIN policy_polobjval ON policy_polrisk."POLID_F" = policy_polobjval."POLID_F"
    LIMIT 100;
"""

cursor.execute(query)
results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(results, columns=columns)

cursor.close()
conn.close()


# --- Filter and convert types ---
df = df[df['PREMIUMSPAY'] > 0]
df['AMOUNT'] = df['AMOUNT'].astype(float)
df['PREMIUMSPAY'] = df['PREMIUMSPAY'].astype(float)
df['CLAIM_RATIO'] = df['AMOUNT'] / df['PREMIUMSPAY']

# --- Plot distribution ---
df['CLAIM_RATIO'].hist(bins=30)
plt.title("Claim Ratio Distribution")
plt.xlabel("Claim Ratio")
plt.ylabel("Frequency")
plt.show()

threshold = df['CLAIM_RATIO'].quantile(0.75)
df['HIGH_RISK'] = df['CLAIM_RATIO'].apply(lambda x: 1 if x >= threshold else 0)

print("[INFO] Claim Ratio Threshold for High Risk:", threshold)
print("[INFO] Target class distribution:\n", df['HIGH_RISK'].value_counts())



if df['HIGH_RISK'].nunique() > 1:

    available_features = ['RATE', 'PREMIUMS', 'PREMIUMSPAY']
    X = df[available_features]
    y = df['HIGH_RISK']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

else:
    print("[WARNING] Only one class found in 'HIGH_RISK'. Model training skipped.")

import matplotlib.pyplot as plt


features = ['AMOUNT', 'AGE', 'TRUSTED']
feature_importance = model.feature_importances_
sorted_idx = np.argsort(feature_importance)
plt.barh(np.array(features)[sorted_idx], feature_importance[sorted_idx])
plt.xlabel("Importance")
plt.title("Feature Importance in GBM")
plt.show()


# X = df_cleaned.drop('RATE', axis=1)
# y = df_cleaned['RATE']
#
# X = X.select_dtypes(include=['number'])
#
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error (MSE) for GradientBoostingRegressor: {mse}')






#
# # print(accurancy_score(y_test, y_pred))
#
# #Logistic Regression
#
# lod_reg = LogisticRegression()
# log_reg.fit(X_train, y_train)
# y_log_reg_pred = log_reg.predict(X_test)
#
#
#
#
# #RandomForestClassifier
#
# random_forest = RandomForestClassifier()
# random_forest.fit(X_train, y_train)
#
# importances = random_forest.feature_importances_
# feature_names = X.columns
# sorted = importances.argsort()
#
# plt.figure(figsize=(10, 6))
# plt.barh(range(len(sorted)), importances[sorted], align="center")
# plt.yticks(range(len(sorted)), feature_names[sorted])
# plt.xlabel("Feature Importance")
# plt.title("Important Factors in Customer Churn")
# plt.show()
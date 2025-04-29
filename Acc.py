from itertools import groupby


import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("C:/Users/it.usnak/Desktop/accounting_account.csv")
df_ledger = pd.read_csv("C:/Users/it.usnak/Desktop/accounting_ledger.csv")


# df["OPENDATE"] = pd.to_datetime(df["OPENDATE"])
# df = df.sort_values("OPENDATE")
# df["time_diff"] = df["OPENDATE"].diff().dt.total_seconds() / 3600
#
# average_freq = df["time_diff"].mean()
# print("On average a new account is created every ", average_freq, " hours")





# print(df["LEDGER_F"])
#
# count = df["LEDGER_F"].value_counts().head(5)
# print(count)
#
# df_merged = pd.merge(df, df_ledger, left_on="LEDGER_F", right_on="LEDGER")
#
# df_selected = df_merged[["LEDGER_F", "NAME_A_y"]]
#
# print(df_selected.head())
#
# df_filtered = df_selected[df_selected["LEDGER_F"].isin([70, 8050, 8051, 36, 1010011])]
# df_filtered_unique = df_filtered.drop_duplicates(subset=["LEDGER_F", "NAME_A_y"])
# print(df_filtered_unique)



# df["OPENDATE"] = pd.to_datetime(df["OPENDATE"])
# df = df.sort_values("OPENDATE")
#
# acc_created = df.groupby(df["OPENDATE"].dt.date).size()
#
# max_creation_day = acc_created.idxmax()
# max_creation_count = acc_created.max()
#
# print(f"The day with the most account creations is {max_creation_day} with {max_creation_count} accounts created.")






# df["OPENDATE"] = pd.to_datetime(df["OPENDATE"])
# acc_created = df.groupby(df["OPENDATE"].dt.date).size()
# acc_created = acc_created[acc_created.index > pd.to_datetime('2011-12-31').date()]
#
# plt.figure(figsize = (10,5))
# plt.plot(acc_created.index, acc_created.values)
# plt.xlabel("Date")
# plt.ylabel("Number of new Accounts")
# plt.title("Accounts Created Over Time")
# plt.grid(True)
# plt.show()


df_user = pd.read_csv("C:/Users/it.usnak/Desktop/auth_user.csv")
# print(df_user.info())
#
# df_user["last_login"] = pd.to_datetime(df_user["last_login"])
# df_user["date_joined"] = pd.to_datetime(df_user["date_joined"])
#
# abandoned_users = df_user[(df_user['last_login'].isna()) | (df_user['last_login'] == df_user['date_joined'])]
# df_user['last_login'] = df_user['last_login'].dt.tz_localize(None)
# inactive_users = df_user[df_user['last_login'] < pd.Timestamp.today() - pd.DateOffset(months=12)]
#
# print(f"Abandoned accounts: {len(abandoned_users)}")
# print(f"Inactive accounts (12+ months): {len(inactive_users)}")




df_cont = pd.read_csv("C:/Users/it.usnak/Desktop/customer_custcontract.csv")
df_customer = pd.read_csv("C:/Users/it.usnak/Desktop/customer_customer.csv")
# print(df_cont.info())

# df_cont["FDATE"] = pd.to_datetime(df_cont["FDATE"])
# df_cont["STOPDATE"] = pd.to_datetime(df_cont["STOPDATE"])
#
# df_cont["lifespan"] = (df_cont["STOPDATE"] - df_cont["FDATE"]).dt.days
#
# income_per_customer = df_cont.groupby('CUST_F')['MAXPREMIUM'].sum().reset_index()
# lifespan_per_customer = df_cont.groupby('CUST_F')['lifespan'].mean().reset_index()
#
# customer_ltv = pd.merge(income_per_customer, lifespan_per_customer, on='CUST_F')
# customer_ltv['LTV'] = customer_ltv['MAXPREMIUM'] / customer_ltv['lifespan']
#
#
# customer_ltv = pd.merge(customer_ltv, df_customer, left_on="CUST_F", right_on="CUSTOMER")
# customer_ltv = customer_ltv[['CUSTOMER', 'NAME_A', 'LTV']]
#
# print(customer_ltv.sort_values(by='LTV', ascending=False).head(20))


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



df_cont["FDATE"] = pd.to_datetime(df_cont["FDATE"])
df_cont["STOPDATE"] = pd.to_datetime(df_cont["STOPDATE"])

customer_premium = df_cont.groupby('CUST_F')['MAXPREMIUM'].sum().reset_index()
customer_premium.rename(columns={'MAXPREMIUM': 'total_premium'}, inplace=True)

threshold = customer_premium['total_premium'].quantile(0.90)
high_value_customers = customer_premium[customer_premium['total_premium'] >= threshold]

high_value_customers = pd.merge(high_value_customers, df_customer, left_on="CUST_F", right_on="CUSTOMER")
high_value_customers = high_value_customers[['CUSTOMER', 'NAME_A', 'total_premium']]

print("Top High-Value Customers:")
print(high_value_customers.sort_values(by='total_premium', ascending=False).head(10))



# import matplotlib.pyplot as plt
# import seaborn as sns
#
# plt.figure(figsize=(10,5))
# sns.histplot(customer_ltv['LTV'], bins=30, kde=True)
# plt.xlabel("Lifetime Value (LTV)")
# plt.ylabel("Number of Customers")
# plt.title("Customer LTV Distribution")
# plt.show()



plt.figure(figsize=(10, 5))
sns.histplot(customer_premium['total_premium'], bins=15, kde=True)
plt.axvline(threshold, color='red', linestyle='dashed', linewidth=2, label='90th Percentile')
plt.xlabel("Total Premium Paid")
plt.ylabel("Number of Customers")
plt.title("Distribution of Customer Premiums")
plt.legend()
plt.show()




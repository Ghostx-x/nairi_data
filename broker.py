import pandas as pd
import matplotlib.pyplot as plt


# policy_risk = pd.read_csv("C:/Users/it.usnak/Desktop/policy_polrisk.csv")
# broktype = pd.read_csv("C:/Users/it.usnak/Desktop/brok_broktype.csv")
#
# df = policy_risk.merge(broktype, left_on="BTYPE_RID_F", right_on="ID", how="left")
# broker_sales = df.groupby(["ID_x", "NAME_A"])["SALE"].sum().reset_index()
# broker_sales = broker_sales.sort_values(by="SALE", ascending=False)
#
# print(broker_sales)
#
#
# print(broker_sales.head(10))
#
# plt.figure(figsize=(12, 6))
# plt.barh(broker_sales["NAME_A"][:10], broker_sales["SALE"][:10], color="skyblue")
# plt.xlabel("Total Sales")
# plt.ylabel("Broker Name")
# plt.title("Top 10 Brokers by Policy Sales")
# plt.gca().invert_yaxis()
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# policy_risk = pd.read_csv("C:/Users/it.usnak/Desktop/policy_polrisk.csv")
# customer = pd.read_csv("C:/Users/it.usnak/Desktop/customer_customer.csv")
#
# customer["AGE"] = 2025 - pd.to_datetime(customer["BIRTHDAY"], errors='coerce').dt.year
# #customer_trends = customer.groupby(pd.cut(customer["AGE"], bins=[18, 30, 40, 50, 60, 100]))["SALE"].sum()
#
#
# df = policy_risk.merge(customer, left_on="CUSTOMER", right_on="AGE", how="left")
#
# customer_trends = df.groupby("AGE", as_index=False)["SALE"].sum()
#
# customer_trends = customer_trends.sort_values(by="SALE", ascending=False)
#
# print(customer_trends.head(10))
#
#
# plt.figure(figsize=(12, 6))
# plt.barh(customer_trends["AGE"][:10], customer_trends["SALE"][:10], color="skyblue")
# plt.xlabel("Total Sales")
# plt.ylabel("Customer Type")
# plt.title("Top 10 Customer Types by Policy Sales")
# plt.gca().invert_yaxis()
# plt.show()


coef = pd.read_csv("C:/Users/it.usnak/Desktop/polcont_poldcoefcst.csv")

mean_coef = coef['COEFCENT'].mean()
std_coef = coef['COEFCENT'].std()

low = mean_coef - 2 * std_coef
high = mean_coef + 2 * std_coef

unusual = coef[(coef["COEFCENT"] < low) | (coef["COEFCENT"] > high)]
print(unusual)



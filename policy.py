import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

policy_risk = pd.read_csv("C:/Users/it.usnak/Desktop/policy_polrisk.csv")
polcont_poldet = pd.read_csv("C:/Users/it.usnak/Desktop/polcont_poldet.csv")
broktype = pd.read_csv("C:/Users/it.usnak/Desktop/brok_broktype.csv")
poldetclause = pd.read_csv("C:/Users/it.usnak/Desktop/polcont_poldetclause.csv")

print(policy_risk.columns)


policy_risk['PREMIUM_NOTPAYED'] = policy_risk['PREMIUMS'] - policy_risk['PREMIUMSPAY']

sorted_policy_risk = policy_risk[['PREMIUM_NOTPAYED', 'POLID_F']].sort_values(by='PREMIUM_NOTPAYED', ascending=True)
print(sorted_policy_risk.to_string(index=False))
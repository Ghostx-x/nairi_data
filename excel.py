import pandas as pd

# Data in a dictionary format
data = {
    'REGION': ['YR', 'KT', 'AM', 'AR', 'SY', 'SH', 'VD'],
    'LocationName': ['Yerevan Region', 'Kotayk Region', 'Ararat Region', 'Armavir Region',
                     'Syunik Region', 'Shirak Region', 'Vayots Dzor Region']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame as an Excel file
df.to_excel('regions.xlsx', index=False)

print("Excel file 'regions.xlsx' created successfully.")

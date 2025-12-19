import pandas as pd

df = pd.read_csv('vietnam_2023_only.csv')
df = df.iloc[:, :-2]

# Optionally, save the modified DataFrame to a new CSV
df.to_csv('vietnam_2023_modified.csv', index=False)

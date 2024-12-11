import pandas as pd
import re

df = pd.read_csv('new_laptops.csv')
new_df = pd.DataFrame({'Name':[],'Link':[]})
df=df.sort_values(by='Performance',ascending=True)
name = 'OLED'

for i in range(len(df)):
    string = df.iloc[i,0]
    if re.search(r'\b'+name+r'\b',string):
        print(df.iloc[i,1])
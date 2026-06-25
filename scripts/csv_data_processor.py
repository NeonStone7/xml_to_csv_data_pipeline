import pandas as pd

pd.set_option('display.max.columns', None)

file = 'datasets\output_data\DLTINS_20210118_01of01.csv'
df = pd.read_csv(file)

df['a_count'] = df['FullNm'].apply(lambda x: x.lower().count('a')).fillna(0)
df['contains_a'] = df['a_count'].apply(lambda x: 'YES' if x>1 else 'NO')

x = df[df['a_count']==0]
print(x[['FullNm', 'a_count', 'contains_a']])
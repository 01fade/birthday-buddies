import os
import pandas as pd
from datetime import datetime

path = 'download'
files = os.listdir(path)

print(files)

df_list = []
rows = 0
for file in files:
    if "csv" in file:
    	print(file)
    	df = pd.read_csv("./" + path + "/" + file)
    	rows += df.count()[0]
    	# print(df)
    	print(df.count()[0], rows)
    	df_list.append(df)

bdf = pd.concat(df_list, ignore_index=True)
bdf.sort_values(by=['sitelinks'])
bdf.to_csv("Combined.csv", index=False)

bdf = bdf.drop_duplicates(subset=['qid'])
print(bdf.count())

filter1 = (bdf['sitelinks'] >= 30) & (bdf['sitelinks'] < 40) & ~(bdf['dateInfo'].str.len() > 0)

df30 = bdf[filter1]
df30 = df30.drop(columns=['dateInfo'])
# df30.to_csv("Combined30-40.csv", index=False)

# print(df30.count())

filter2 = (bdf['sitelinks'] >= 40) & ~(bdf['dateInfo'].str.len() > 0)

df40 = bdf[filter2]
df40 = df40.drop(columns=['dateInfo'])

# print(df40.count())
# print(df30[~(df30['label'].str.len() > 0)])

def formatDate(x):
	dates = x.split("|")
	formattedDate = []
	for d in dates:
		dobj = datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')
		darr = [dobj.year, dobj.month, dobj.day]
		formattedDate.append("-".join(map(str, darr)))
	return "|".join(formattedDate)

df40['date'] = df40['date'].apply(formatDate)
# df40 = df40.drop(columns=['place', 'territory', 'country', 'coordinates', 'image'])
df40.to_csv("Combined40.csv", index=False)

print(df40)
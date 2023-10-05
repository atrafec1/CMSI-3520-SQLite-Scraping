import mechanicalsoup
import pandas as pd
import sqlite3

url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
browser = mechanicalsoup.StatefulBrowser()
browser.open(url)

th = browser.page.find_all("th", attrs={"scope": "row"})
rank = [value.text.replace("\n", "") for value in th]
rank = rank[:333]

td = browser.page.find_all("td")
columns = [value.text.replace("\n", "") for value in td]
columns = columns[18:3348]
print(columns)
print(columns[len(columns)-1])

column_names = ["City",
                "State",
                "2022_Estimate",
                "2022_Census", 
                "Change", 
                "2020_Land_Area", 
                "2020_Population_Density", 
                "Location" 
                ]

# # column[0:][::11]
# # column[1:][::11]
# # column[2:][::11]

dictionary = {"2022_Rank": rank}

for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::8]


df = pd.DataFrame(data = dictionary)
# print(df.head())
# print(df.tail())

connection = sqlite3.connect("distro.db")
cursor = connection.cursor()
cursor.execute("create table linux (Distribution, " + ",".join(column_names) + ")")
for i in range(len(df)):
    cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])

connection.commit()

connection.close()
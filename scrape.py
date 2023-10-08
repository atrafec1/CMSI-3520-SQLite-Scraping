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







#3348



column_names = ["City",
                "State",
                "The_2022_Estimate",
                "The_2022_Census", 
                "Change", 
                "The_2020_Land_Area",
                "not_needed",
                "The_2020_Population_Density",
                "not_needed2",
                "Location" 
                ]

# # column[0:][::11]
# # column[1:][::11]
# # column[2:][::11]

dictionary = {"The_2022_Rank": rank}

for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::10]

dictionary.pop("not_needed")
dictionary.pop("not_needed2")
column_names.remove("not_needed")
column_names.remove("not_needed2")



df = pd.DataFrame(data = dictionary)

connection = sqlite3.connect("distro.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS linux")
cursor.execute("create table linux (Rank, " + ",".join(column_names) + ")")
for i in range(len(df)):
    cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?)", df.iloc[i])

connection.commit()

connection.close()
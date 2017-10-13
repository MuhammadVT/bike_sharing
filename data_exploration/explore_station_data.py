#!/bin/sh

import folium
import pandas as pd
import matplotlib.pyplot as plt
import imgkit
from html_to_png import html_to_png

# select ggplot style
plt.style.use("ggplot")

# read data into a pandas dataframe
df_station = pd.read_csv("../data/station.csv", parse_dates=["installation_date"])

# geo_path = df_station

####################################################
## plot the city map
#city_map = folium.Map(location=[df_station.lat.mean(), df_station.long.mean()],
#                      zoom_start=10)
#
## aggregate by city and take the mean value
#dfn = df_station.groupby(by='city', as_index=False).mean()
#
## mark the cities
#for idx, row in dfn.iterrows():
#    folium.Marker([row['lat'], row['long']]).add_to(city_map)
#output_html = "./screenshots/city_map.html"
#city_map.save(output_html)
#
##config = imgkit.config(wkhtmltoimage="/usr/local/bin/wkhtmltoimage-amd64")
##config = imgkit.config(wkhtmltoimage="/usr/bin/wkhtmltopdf")
##imgkit.from_file("map.html", "map.jpg", config=config)
##imgkit.from_file("map.html", "map.jpg")
#html_to_png(output_html, output_png="./screenshots/city_map.png")

#################################################

####################################################
## plot the stations on a map
#station_map = folium.Map(location=[df_station.lat.mean(), df_station.long.mean()],
#                      zoom_start=10)
#
## aggregate by station name and take the mean value
#dfn = df_station.groupby(by='name', as_index=False).mean()
#
## mark the cities
#for idx, row in dfn.iterrows():
#    folium.Marker([row['lat'], row['long']]).add_to(station_map)
#output_html = "./screenshots/station_map.html"
#station_map.save(output_html)
#
##config = imgkit.config(wkhtmltoimage="/usr/local/bin/wkhtmltoimage-amd64")
##config = imgkit.config(wkhtmltoimage="/usr/bin/wkhtmltopdf")
##imgkit.from_file("map.html", "map.jpg", config=config)
##imgkit.from_file("map.html", "map.jpg")
#output_png = "./screenshots/station_map.png"
#html_to_png(output_html, output_png=output_png)
#
#
######################################################

###############################################################
## plot the dock number versus station
#fig, ax = plt.subplots(figsize=(20, 2))
#df_station.plot(ax=ax, x=["name"], y=["dock_count"], kind="bar")
#
## set x, y labels
#ax.set(xlabel="Station", ylabel="Dock Count")
#
## rotate the x-axis tick labels
##ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=20)
#
## hide the lagends
#ax.legend().set_visible(False)
#
#plt.show()
###############################################################


###############################################################
# plot the dock number versus station
fig, ax = plt.subplots(figsize=(20, 4))
#df_station.plot(ax=ax, x=["name"], y=["installation_date"], kind="scatter")
#df_station.plot(ax=ax, x=["id"], y=["installation_date"], kind="scatter")
ax.plot(df_station.installation_date, df_station.id, "o")

# set x, y labels
ax.set(xlabel="Station", ylabel="Day of Installation")

# rotate the x-axis tick labels
#ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=30)
ax.set_yticklabels(df_station.name)

# hide the lagends
ax.legend().set_visible(False)

plt.show()


###############################################################


## plot the number of stations per city 
#dfn = df_station.groupby(by='city', as_index=False).count()
#fig, ax = plt.subplots()
#dfn.plot(ax=ax, x=['city'], y=['id'], kind="bar")
#
## set x, y labels
#ax.set(xlabel="City", ylabel="# of Stations")
#
## rotate the x-axis tick labels
#ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=20)
#
## hide the lagends
#ax.legend().set_visible(False)
#
## plot the number of docks per city
#dfn = df_station.groupby(by='city', as_index=False).sum()
#fig, ax = plt.subplots()
#dfn.plot(ax=ax, x=['city'], y=['dock_count'], kind="bar")
#
## set x, y labels
#ax.set(xlabel="City", ylabel="# of Docks")
#
## rotate the x-axis tick labels
#ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=20)
#
## hide the lagends
#ax.legend().set_visible(False)
#plt.show()



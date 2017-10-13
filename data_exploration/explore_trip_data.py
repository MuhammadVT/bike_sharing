# import the necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib

# choose ggplot stype
matplotlib.style.use("ggplot")

# read the trip data into a pandas dataframe
df_trip = pd.read_csv("../data/trip.csv")


# plot the histogram of duration in minutes
# convert duration's unit from second to minute
df_trip.duration.apply(lambda x: x/60.)

# remove the outliers
fig, ax = plt.subplots()
df_trip.hist(column="duration", ax=ax, bins=20)













plt.show()

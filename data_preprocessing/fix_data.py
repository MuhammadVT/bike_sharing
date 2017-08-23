def fix_weather_data():
    """ fixes problems in the weather data in .csv files.
    The fixed file is named as weather_fixed.
    Note: weather data in database.sqlite has been fixed using
    sqlite manager in firefox. The fixed weather data is
    in weather_fixed table. BUT, the fixes in sqlite db may not be up-to-date
    compared to that in weather_fixed.csv. Therefore use weather_fixed.csv.
    """

    import sqlite3
    import pandas as pd

    # Change "rain" to "Rain" in the 'events' column .csv file
    df = pd.read_csv("../data/weather.csv")
    df.loc[:, "events"] = df.events.apply(lambda x: "Rain" if x == "rain" else x)

    # change "T" to "0.005" in precipitation_inches.
    # "T"= trace when amount less than .01 inch"
    df.loc[:, "precipitation_inches"] = df.precipitation_inches.\
                                        apply(lambda x: "0.005" if x == "T" else x)

    # write the fixed data in to weather_fixed.csv file
    df.to_csv("../data/weather_fixed.csv", index=False)

    return

if __name__ == "__main__":
    fix_weather_data()
    

    

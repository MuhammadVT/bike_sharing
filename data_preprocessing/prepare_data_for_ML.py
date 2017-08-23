class prepare_data_for_ML(object):
    def __init__(self, status_data_path="../data/status_time_res_15min.csv",
                 weather_data_path="../data/weather_fixed.csv",
                 station_ids=None,
                 nrows=None):

        """ Prepares the data for various ML models.

        Parameters
        ----------
        status_data_path : str
            Path to status data in csv format 
        weather_data_path : str
            Path to weather data in csv format 
        station_ids : list
            A list of the station ids for which data points are selected.
            Default to None, in which case all the data points will be read.
        nrows : int
            The number of rows (data points) to be read.
            Default to None, in which case all the data points will be read.

        Returns
        -------
            prepare_data_for_ML object
        
        """
        
        import pandas as pd
        import numpy as np

        # read various datasets 
        # read status data
        if status_data_path:
            self.status_data = pd.read_csv(status_data_path, nrows=nrows,
                                           parse_dates=["time"])
            if station_ids:
                idx_bool = self.status_data.station_id.apply(lambda x:\
                                True if x in station_ids else False)
                self.status_data = self.status_data.loc[idx_bool]
        else:   
            self.status_data = None 

        # read weather data
        if weather_data_path:
            self.weather_data = pd.read_csv(weather_data_path, nrows=nrows,
                                            parse_dates=["date"])
        else:   
            self.weather_data = None


    def prepare_data_for_RF(self):
        """ prepares data for Random Forest Regression """
        
        if self.status_data is not None:
            # copy status data
            df = self.status_data
            
            # drops some columns
            df.drop(["docks_available"], axis=1, inplace=True)

            # remove the last row where there is no entry for bikes_available_future
            df.drop(df.index[-1], inplace=True)
            
            # add features from status data
            df.loc[:, "time_of_day"] = df.time.apply(lambda x: x.strftime("%H:%M"))
            df.loc[:, "day_of_week"] = df.time.apply(lambda x: x.weekday())
            df.loc[:, "month_of_year"] = df.time.apply(lambda x: x.month)

            def extract_same_day_weather_data(x, weather_dates):
                row_indx = self.weather_data.index[\
                           weather_dates == x.date()]
                return row_indx[0]
                
            #tm_bool = df.time.apply(lambda x: x.date()) == \
            #          self.weather_data.date.apply(lambda x: x.date())

            # get all the dates in the weather data
            weather_dates = self.weather_data.date.apply(lambda x: x.date()).as_matrix()

            # add features from weather data
            features_list = ["mean_temperature_f", "mean_humidity",
                             "mean_visibility_miles", "mean_wind_speed_mph",
                             "precipitation_inches", "events"]
            indices = [extract_same_day_weather_data(x, weather_dates) for x in df.time]
            for f in features_list:
                df.loc[:, f] = (self.weather_data.loc[indices, f]).as_matrix()

            # add the bikes_available_future (i.e, bikes_available in the next data point)
            #  which we will predict
            df.loc[:, "bikes_available_future"] = df.bikes_available.shift(-1).as_matrix()

            # drop time column
            df.drop(["time"], axis=1, inplace=True)
            
        else:
            df = None

        return df

# test code
if __name__ == "__main__":
    nrows = 100
    station_ids = [2]
    obj = prepare_data_for_ML(nrows=nrows, station_ids=station_ids)
    df = obj.prepare_data_for_RF()
      

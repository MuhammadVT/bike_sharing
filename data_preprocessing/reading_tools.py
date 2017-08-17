def read_data_from_db(stm, etm, station_id, time_res="1"):
    """ reads data (time resolution set by rime_res) from an sqlite3 db
    for a period of time (set by stm and etm) for a given station_id.
    
    Parameters
    ----------
    stm : datetime.datetime
        The start time
    etm : datetime.datetime
        The end time
    station_id : int
        The station id
    time_res : str
        Time resolution.
        
    Returns
    -------
    pandas.DataFrame
    """

    import sqlite3
    import pandas as pd
    
    # construct db name and table name
    if time_res == "1":
        db_name = "../data/database.sqlite"
        table_name = "status"
    else:
        db_name = "../data/sampled_data.sqlite"
        table_name = "time_res_" + str(time_res) + "min"

    # make db connection
    conn = sqlite3.connect(database=db_name)

    #sql = table_name
    sql = "SELECT * FROM {tb} WHERE station_id={station_id} AND "
    sql = sql + "(DATETIME(time) BETWEEN '{stm}' and '{etm}')"
    sql = sql.format(tb=table_name, station_id=station_id, stm=stm, etm=etm)
    
    # get the data we want in a pandas DataFrame format
    df = pd.read_sql(sql, conn, index_col=None, coerce_float=True, params=None,
                  parse_dates=["time"], columns=None, chunksize=None)
    
    return df

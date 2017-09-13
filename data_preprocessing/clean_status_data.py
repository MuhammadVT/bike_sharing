# load the packages
import sqlite3
import pandas as pd
import numpy as np
import datetime as dt
import multiprocessing as mp

def fix_time_format(input_dbname="../data/database.sqlite",
                    output_dbname="../data/database_fixed.sqlite",
                    input_tablename="status",
                    output_tablename="status"):
    """fixses the time format in the original db and writes the
    fixed data into a new db"""

    # make db connection
    conn = sqlite3.connect(input_dbname)
    cur = conn.cursor()

    # make db connection
    conn_new = sqlite3.connect(output_dbname)
    cur_new = conn_new.cursor()

    # create a table
    colname_type = "station_id INTEGER, bikes_available INTEGER,\
                    docks_available INTEGER, time TIMESTAMP,\
                    CONSTRAINT status_pk PRIMARY KEY (station_id, time)"
    command = "CREATE TABLE IF NOT EXISTS {tbn} ({colname_type})"\
              .format(tbn=output_tablename, colname_type=colname_type)
    cur_new.execute(command)

    # extract data from status table in database.sqlite
    command = "SELECT station_id, bikes_available, docks_available,\
               time FROM {tb}".format(tb=input_tablename)
    cur.execute(command)

    # build insert command
    cols = "station_id, bikes_available, docks_available, time"
    command_insert = "INSERT or IGNORE INTO {tbn} ({cols}) VALUES (?, ?, ?, ?)"
    command_insert = command_insert.format(tbn=output_tablename, cols=cols)

    # iterate through each data point
    rw = cur.fetchone()
    k = 0
    while rw:
        # convert string to python datetime object
        try:
            tm_tmp = dt.datetime.strptime(rw[-1], "%Y/%m/%d %H:%M:%S")
        except:
            tm_tmp = dt.datetime.strptime(rw[-1], "%Y-%m-%d %H:%M:%S")
        
        # set the second to 0
        tm_tmp = tm_tmp.replace(second=0)

        # populate the table
        rw_new = tuple([rw[0], rw[1], rw[2], tm_tmp])
        cur_new.execute(command_insert, rw_new)
        
        k = k + 1
        if k==10000:
            print("Inserting " + str(rw_new))
            k = 0

        # read the next record
        rw = cur.fetchone()

    # commit the chage
    conn_new.commit()

    # close db connections
    conn.close()
    conn_new.close()

    return

def insert_missing_points(db_name="../data/database_fixed.sqlite"):
    """ inserts a data point at every minute.
    Fills the missing data with NaN values. """

    pass

#    # make db connection
#    conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
#    cur = conn.cursor()
#    
#    command = "SELECT station_id FROM {tb} GROUP BY station_id" 
#    cur.execute(command)
#    rows = cur.fetchall()
#    station_ids = [x[0] for x in rows] 
#
#    for id in station_ids:
#        
#        # get the start time
#        command = "SELECT station_id, time FROM {tb} ORDER By ASC time LIMIT 1" 
#        cur.execute()
#        rw = cur.fetchall()[0]
#        stm = rw[[1] 
#
#        # get the end time
#        command = "SELECT station_id, time FROM {tb} ORDER By DESC time LIMIT 1" 
#        cur.execute()
#        rw = cur.fetchall()[0]
#        etm = rw[1]
#        
#
#    # close db connection
#    conn.close()
#
#
#    return

# run the code
def main():

    # fix the time format and write the fixed data into a new db
    fix_time_format(input_dbname="../data/database.sqlite",
                    output_dbname="../data/database_fixed.sqlite",
                    input_tablename="status",
                    output_tablename="status_time_res_1min")

    return

if __name__ == "__main__":
    main()


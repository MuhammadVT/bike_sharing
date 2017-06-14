import sqlite3
import csv

def sqlite_to_csv(dbname, tbname, outfile):
    """ convert a table in an sqlite3 db into a .csv file
    Parameters
    ----------
    dbname : str
        file path + db name
    tbname : str
        Name of a table whose content will be converted into a .csv file
    outfile : str
        file path + .csv name

    Returns
    -------
    Nothing
    
    """

    with sqlite3.connect(dbname) as conn:
        csv_writer = csv.writer(open(outfile, "w"))
        cur = conn.cursor()

        # fetch the data
        command = "SELECT * FROM {tb}". format(tb=tbname)
        cur.execute(command)
        rws = cur.fetchall() 

        # write to .csv file
        csv_writer.writerows(rws)

        return


# run the code
dbname = "../data/sampled_data.sqlite"
tbname = "time_res_5min"
outfile = "../data/status_time_res_15min.csv"
sqlite_to_csv(dbname, tbname, outfile)

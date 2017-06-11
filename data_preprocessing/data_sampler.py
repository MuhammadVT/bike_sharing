# load the packages
import sqlite3
import pandas as pd
import numpy as np
import datetime as dt
import multiprocessing as mp


def sampler(time_res=15, n_jobs=None):
    """ This function reduces the size of the status data by
    sampling at every time_res minutes. The output is returned as a dataframe
    
    Parameters
    ----------
    time_res : int
        time resolution in minutes, default to 15 minutes
    n_jobs : int
        The number of jobs to run in parallel. If set to None, 
        then the number of jobs is set to the number of cores.
        Defulat value is -1.

    Return
    ------
    Pandas DataFrame

    """

    # number of jobs to be run in parallel
    if not n_jobs:
        n_jobs = mp.cpu_count()

    # make db connection
    conn = sqlite3.connect("../data/database.sqlite")
    cur = conn.cursor()

    # get the total number of data points in status table
    command = "SELECT Count(station_id) FROM {tb}".format(tb="status")
    cur.execute(command)
    npnts = cur.fetchone()[0]

    # Define an output queue
    output = mp.Queue()

    # batch size for each job (process)
    batch_size = int(np.ceil(1.0 * npnts / n_jobs)) 

    # extract data from status table in database.sqlite
    command = "SELECT station_id, bikes_available, docks_available,\
               time FROM {tb}".format(tb="status")
    cur.execute(command)

    # since the data size is large, we run the n_jobs in parallel
    procs = []
    for pos in range(n_jobs):
        batch = cur.fetchmany(batch_size)
        p = mp.Process(target=worker, args = (batch, time_res, pos, output))
        procs.append(p)
        p.start()

    # exit the completed processes
    for p in procs:
        p.join()
    
    # collect the results of each process
    data = [output.get() for p in procs]

    # flatted the list of lists
    data = [x for lst in data for x in lst[1]]

    # sort by time
    data.sort(key=lambda x: x[-1])

    # convert list into dictionary
    kys = ["station_id", "bikes_available", "docks_available", "time"]
    data = {kys[i]: [x[i] for x in data] for i in range(len(kys)) }

    # Create a dataframe
    df = pd.DataFrame(data=data)
    df.set_index('time')

    return df

def worker(batch, time_res, pos, output):
    """ A worker function that will be fed into the Multiprocessing module
    for parallel computing

    Parameters
    ----------
    batch : Cursor
        Holds the outputs of an sqlite query
    time_res : int
        Time resolution in minutes, default to 15 minutes
    pos : int
        order of a process
    outpur : Multiprocessing.Queue object
        Stores the output of multiprocesses 

    Return
    ------
    List
        A list of tuples
    """

    data = []

    # since data size is large we do not fetchall, but, instead,
    # loop through the elements in batch 
    for rw in batch:

        # convert string to python datetime object
        try:
            tm_tmp = dt.datetime.strptime(rw[-1], "%Y/%m/%d %H:%M:%S")
        except:
            tm_tmp = dt.datetime.strptime(rw[-1], "%Y-%m-%d %H:%M:%S")

        # sample the data at every time_res minutes
        if not tm_tmp.minute % time_res:
            tm_tmp = tm_tmp.replace(second=0)           # set seconds to zero
            data.append(tuple(list(rw[:-1]) + [tm_tmp]))

    return output.put((pos, data))

# run the code
df = sampler(time_res=15, n_jobs=None)



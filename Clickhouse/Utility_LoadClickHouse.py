from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import time
from termcolor import colored


def CalculateAvgTemperatureOutside():
    if any(loaddata['hp2_temperatureOutside'].isna()) == True:
        return loaddata['hp1_temperatureOutside']
    else:
        return (loaddata['hp1_temperatureOutside'] + loaddata['hp2_temperatureOutside'])/2    


def CalculateCOP(loaddata):
    if all(loaddata['hp1_thermalEnergyCounter'] > 0) and all(loaddata['hp1_electricalEnergyCounter'] > 0) and all(loaddata['qc_cvEnergyCounter']): 
        if any(loaddata['hp2_thermalEnergyCounter'].isna()) == True and any(loaddata['hp2_electricalEnergyCounter'].isna()==True):
            return loaddata['hp1_thermalEnergyCounter'] / loaddata['hp1_electricalEnergyCounter']
        else:
            return (loaddata['hp1_thermalEnergyCounter'] + loaddata['hp2_thermalEnergyCounter']) / (loaddata['hp1_electricalEnergyCounter'] + loaddata['hp2_electricalEnergyCounter'])


def get_total_time_range(table, clientid):

    query = f"""
        SELECT
            MIN(time_ts) AS min_time,
            MAX(time_ts) AS max_time
        FROM
            {table}
        WHERE
            clientid = %(clientid)s
    """

    params = {
        'clientid'        : clientid,
    }

    return query, params


def query_define(extractVariables, table, clientid, startTime, endTime):

    columns = ', '.join(extractVariables)

    base_query = f"""
        SELECT
            {columns}
        FROM
            {table}
        WHERE
            clientid = %(clientid)s
    """

    if startTime is not None and endTime is not None:
        base_query += """
            AND time_ts BETWEEN %(startTime)s AND %(endTime)s
        """

    params = {
        'clientid'        : clientid,
        'startTime'       : startTime,
        'endTime'         : endTime
    }

    return base_query, params

    '''
    query = """
        SELECT
            clientid,
            toStartOfFiveMinutes(time_ts) as time,
            argMin(qc_supervisoryControlMode, time_ts) as qc_supervisoryControlMode,
            argMin(hp1_thermalEnergyCounter, time_ts) as hp1_thermalEnergyCounter,
            argMin(hp1_electricalEnergyCounter, time_ts) as hp1_electricalEnergyCounter,
            argMin(qc_cvEnergyCounter, time_ts) as qc_cvEnergyCounter
        FROM
            cic_stats
        WHERE
            clientid = %(cic_id)s
            AND time_ts BETWEEN %(start_time)s AND %(end_time)s
        GROUP BY clientid, toStartOfFiveMinutes(time_ts)
        ORDER BY clientid, toStartOfFiveMinutes(time_ts)
    """

    query2 = """
        SELECT
            time_ts,
            clientid as cic_id,
            qc_minimumCOP,
            hp1_limitedByCop,
            hp2_limitedByCop
        FROM
            cic_stats
        WHERE
            clientid = %(cic_id)s

    """
    query3 = """
        SELECT *
        FROM
            cic_stats
        WHERE
            clientid = %(cic_id)s
            AND time_ts BETWEEN %(start_time)s AND %(end_time)s
    """
    '''


def SaveQueryResult(df, extractVariables, startTime, endTime, clientid, params):
    try:

        if extractVariables != ['*']:
            variables_name = extractVariables
        else:
            variables_name = "AllVariables"

        if startTime != None and endTime != None:
            dt_start = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
            unixtime_start = int(time.mktime(dt_start.timetuple()))
            dt_end = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
            unixtime_end = int(time.mktime(dt_end.timetuple()))
            time_name = f"_{unixtime_start}_{unixtime_end}"
        else:
            time_name = str("")

        Name = f"{variables_name}_{clientid}{time_name}.csv"

        df.to_csv(Name, index=False)
        print(colored("Succesfully saving the file: ", "red") + Name)
        print(colored("Parameters are:", "red"))
        for key, value in params.items():
            value = "None" if value is None else str(value)
            print(key + str(' = ') + value)
    except Exception as e:
        print(f"An error occurred: {e}")


def PlotMatrix(times, loaddata, start_index, end_index):
    for index in range(start_index, end_index):
        plt.figure( figure=(30,18) )
        ax=plt.gca()

        plt.plot(times, loaddata.iloc[:,index])

        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
        ax.tick_params(axis='x', labelsize=30, size=10)

        y_value_name = loaddata.columns[index]
        plt.ylabel(y_value_name, fontsize=60)

        plt.savefig( 'Plots/' + y_value_name + "_" + str(index) + '.png')
        plt.close()


def Plot(x, y, plotname, filename):

    Variables, CIC_id, starttime, endtime = filename.split('_')
    endtime = endtime.replace('.csv', '')

    plt.figure( figure=(30,18) )
    ax=plt.gca()

    plt.scatter(x, y)

    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    ax.tick_params(axis='x', labelsize=30, size=10)
    
    plt.ylabel(plotname, fontsize=60)

    plt.savefig( 'Plots/' + plotname + '_' + CIC_id + '_' + starttime + '_' + endtime + '.png')
    plt.close()


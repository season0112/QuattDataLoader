import clickhouse_connect
from .loadClickHouseCredentials import clickhouse_host, clickhouse_user, clickhouse_password, clickhouse_port
from . import Utility_LoadClickHouse

def connect_clickhouse(arguments):

    client = clickhouse_connect.get_client(
        host     = clickhouse_host,
        user     = clickhouse_user,
        password = clickhouse_password,
        port     = clickhouse_port,
        secure   = True
    )

    # Executing the query
    # Get Min, Max time (To be fixed: for None input)
    if arguments.startTime != None and arguments.endTime != None:
        minTime = arguments.startTime
        maxTime = arguments.endTime
    else:
        query_GetTime, params_GetTime = Utility_LoadClickHouse.get_total_time_range(arguments.table, arguments.clientid)
        df_GetTime = client.query_df(query_GetTime, params_GetTime)
        minTime = df_GetTime['min_time']
        maxTime = df_GetTime['max_time']
    print('\n')
    print(minTime)
    print('\n')
    print(maxTime)

    # Get Values
    query,params = Utility_LoadClickHouse.query_define(arguments.extractVariables,
                                arguments.table,
                                arguments.clientid,
                                arguments.startTime,
                                arguments.endTime)
    
    df = client.query_df(query, params)
    df_sorted = df.sort_index(axis=1)

    print(df_sorted)
    #print(df_sorted.head())
    #print(df_sorted.describe())
    #print(df_sorted.columns)












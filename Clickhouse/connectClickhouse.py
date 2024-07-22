import clickhouse_connect
from .loadClickHouseCredentials import clickhouse_host, clickhouse_user, clickhouse_password, clickhouse_port
from . import Utility_LoadClickHouse
from . import NoutKPIQuery, CommonQuery, CO2Query

def connect_clickhouse(arguments):

    client = clickhouse_connect.get_client(
        host     = clickhouse_host,
        user     = clickhouse_user,
        password = clickhouse_password,
        port     = clickhouse_port,
        secure   = True
    )

    # Execute Query
    if arguments.query == None:
        query, params = CommonQuery.query_define(arguments.extractVariables,
                                    arguments.table,
                                    arguments.clientid,
                                    arguments.startTime,
                                    arguments.endTime)
        
        df = client.query_df(query, params)
    else:
        #df = client.query_df(getattr(CommonQuery, arguments.query)())
        #df = client.query_df(getattr(NoutKPIQuery, arguments.query)(StartTime='2024-01-01 00:00:00', EndTime='2024-01-01 23:59:59', Q_min=100))
        df = client.query_df(getattr(CO2Query, arguments.query)(StartTime='2024-07-01 00:00:00', EndTime='2024-07-02 00:00:00', Q_min=0))

    return df



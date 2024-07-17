import mysql.connector
from mysql.connector import Error
from .loadMysqlCredentials import mysql_host, mysql_user, mysql_password, mysql_port, mysql_database
from . import CommonQuery

def connect_mysql(arguments):

    try:
        connection = mysql.connector.connect(host     = mysql_host,
                                             user     = mysql_user,
                                             password = mysql_password,
                                             database = mysql_database,
                                             port     = mysql_port)

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()

            #CommonQuery.ListDataBases(cursor)
            #CommonQuery.ListTables(cursor)
            #CommonQuery.MartijnCO2Calculation(cursor) 
            #CommonQuery.testQuery(cursor)
            CommonQuery.test2Query(cursor)

    except Error as e:
            print("error out.")
    '''
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    '''












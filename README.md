Quatt Data Loader tool.

This includes Quatt data from AWS S3, Clickhouse, AWS RDS Mysql, and Redis.

Before using this data loader tool, please check if your credentials are properly set.
-- For clickhouse, it load Clickhouse credential named ".clickhouse_env" in your $HOME directoriy.
-- For mysql, it load AWS Mysql credential named ".mysql_env" file in your $HOME directoriy.
-- For S3, it load AWS S3 credential named ".aws" folder in your $HOME directoriy, which includes default config and credentials.
-- For Redis, it load Redis credential named ".redis" in your $HOME directoriy. 

Example usage:
-- clickhouse:
python YourAnalysis.py clickhouse --extractVariables qc_minimumCOP --table cic_stats --clientid CIC-87845a22-3d04-5f8c-8d4e-c1e735a9e472 --startTime "2024-01-02 00:00:00" --endTime "2024-01-02 20:00:00"
python YourAnalysis.py clickhouse --query listDataBases

-- mysql:
python YourAnalysis.py mysql --query exampleQuery 

-- S3:
python YourAnalysis.py s3 --action PrintBuckets

-- redis:
python YourAnalysis.py redis 




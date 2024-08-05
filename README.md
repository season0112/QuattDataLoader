# Quatt Data Loader tool.
This includes Quatt data from AWS S3, Clickhouse, AWS RDS Mysql, and Redis.

##  Credentials
Before using this data loader tool, please check if your credentials are properly set.
* For clickhouse, it load Clickhouse credential named ".clickhouse_env" in your $HOME directoriy.
* For mysql, it load AWS Mysql credential named ".mysql_env" file in your $HOME directoriy.
* For S3, it load AWS S3 credential named ".aws" folder in your $HOME directoriy, which includes default config and credentials.
* For Redis, it load Redis credential named ".redis" in your $HOME directoriy. 

## Example usage
* clickhouse:
  * To extract one example variable: ``python YourAnalysis.py clickhouse --extractVariables qc_minimumCOP --table cic_stats --clientid CIC-87845a22-3d04-5f8c-8d4e-c1e735a9e472 --startTime "2024-01-02 00:00:00" --endTime "2024-01-02 20:00:00"``
  * To extract data through your query: ``python YourAnalysis.py clickhouse --query listDataBases``. You can define your queries in `DataLoader/Clickhouse/CommonQuery.py`

* mysql:
  * To extract data through your query: ``python YourAnalysis.py mysql --query exampleQuery ``. You can define your queries in `DataLoader/Mysql/CommonQuery.py`

* S3:
  * To perform actions like Print objects in Buckets: ``python YourAnalysis.py s3 --action PrintBuckets``. Available actions are given here: `DataLoader/S3/boto3_wrapper.py`

* redis:
  * To extract most recent data: ``python YourAnalysis.py redis``



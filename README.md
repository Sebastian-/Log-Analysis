# Log Analysis Script

A script to analyse the database of a made-up news website.

Answers each of the following questions with a single PSQL query:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

## Requirements 
* Python 3+
* PSQL

## Setup and Usage

Run the following command to setup the database

`psql -d news -f newsdata.sql`

Create the required views then simply call

`python log-analysis.py`

## Required Views

These two views should be created before running the script.

```sql
create view err as
select to_char(log.time, 'FMMonth FMDD, YYYY') as day, count(*) as errors
from log where log.status != '200 OK'
group by day;
```

```sql
create view req as 
select to_char(log.time, 'FMMonth FMDD, YYYY') as day, count(*) as requests
from log 
group by day;
```
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

Run the following command to setup the database:

`psql -d news -f newsdata.sql`

Create the required views and then call:

`python log-analysis.py`

## Required Views

These two views should be created before running the script:

```sql
CREATE OR REPLACE VIEW err AS
SELECT to_char(log.time, 'FMMonth FMDD, YYYY') AS day, count(*) AS errors
FROM log WHERE log.status != '200 OK'
GROUP BY day;
```

```sql
CREATE OR REPLACE VIEW req AS 
SELECT to_char(log.time, 'FMMonth FMDD, YYYY') AS day, count(*) AS requests
FROM log 
GROUP BY day;
```
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

Run:

`python log-analysis.py`

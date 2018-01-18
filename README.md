# Log Analysis Script

## Required Views

The following views must be created before running the script.

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
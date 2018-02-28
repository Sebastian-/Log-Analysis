#!/usr/bin/env python3
"""Queries the news database for answers to the following questions:
    What are tthe most popular three articles of all time?
    Who are the most popular article authors of all time?
    On which days did more than 1% of requests lead to errors?"""
import sys
import psycopg2


def run():
    """Calls querys"""
    top_three_articles()
    top_authors()
    error_days()


def connect(database_name):
    """Connect to the PSQL database.
    Returns a database connection and cursor"""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except psycopg2.Error as e:
        print "Unable to connect to database {}".format(database_name)
        sys.exit(1)


def execute_query(query, database_name, fetchresult=True):
    """Returns the result of executing the query on the given database"""
    db, cursor = connect(database_name)
    cursor.execute(query)
    if fetchresult:
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result
    else:
        cursor.close()
        db.close()
        return


def top_three_articles():
    """Prints the three most accessed articles in the news database"""
    table = execute_query(
        "SELECT articles.title, count(*) AS views \
        FROM articles, log WHERE articles.slug = split_part(log.path, '/', 3) \
        GROUP BY articles.title ORDER BY views DESC LIMIT 3", "news")
    print("The top three articles are: \n")
    for row in table:
        print("{} -- {} views".format(row[0], row[1]))
    print("\n")


def top_authors():
    """Prints all authors in the order based off of the
    number of page views for their articles"""
    table = execute_query(
        "SELECT authors.name, views FROM authors, \
        (SELECT articles.author AS id, count(*) AS views FROM articles, log \
        WHERE articles.slug = split_part(log.path, '/', 3) \
        GROUP BY articles.author) AS subq \
        WHERE authors.id = subq.id ORDER BY views DESC", "news")
    print("Authors ordered by popularity: \n")
    for row in table:
        print("{} -- {} views".format(row[0], row[1]))
    print("\n")


def error_days():
    """Prints all days when more than %1 of site requests failed"""
    execute_query("CREATE OR REPLACE VIEW err AS \
        SELECT to_char(log.time, 'FMMonth FMDD, YYYY') AS day, \
        count(*) AS errors \
        FROM log WHERE log.status != '200 OK' \
        GROUP BY day;", "news", False)
    execute_query("CREATE OR REPLACE VIEW req AS \
        SELECT to_char(log.time, 'FMMonth FMDD, YYYY') AS day, \
        count(*) AS requests \
        FROM log  \
        GROUP BY day;", "news", False)
    table = execute_query(
        "SELECT err.day, cast(err.errors AS float) / req.requests * 100 \
        FROM err, req \
        WHERE err.day = req.day \
        AND cast(err.errors AS float) / req.requests > 0.01", "news")
    print("Days where more than 1% of requests failed: \n")
    for row in table:
        print("{0:s} -- {1:.2f}% errors".format(row[0], row[1]))
    print("\n")


if __name__ == '__main__':
    run()

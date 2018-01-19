#!/usr/bin/env python3
"""Queries the news database for answers to the following questions:
    What are tthe most popular three articles of all time?
    Who are the most popular article authors of all time?
    On which days did more than 1% of requests lead to errors?"""

import psycopg2


def run():
    """Calls querys"""
    top_three_articles()
    top_authors()
    error_days()


def top_three_articles():
    """Prints the three most accessed articles in the news database"""
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute("select articles.title, count(*) as views \
        from articles, log where articles.slug = split_part(log.path, '/', 3) \
        group by articles.title order by views desc limit 3")
    print("The top three articles are: \n")
    for table in cursor.fetchall():
        print("{} -- {} views".format(table[0], table[1]))
    print("\n")
    db.close()


def top_authors():
    """Prints all authors in the order based off of the
    number of page views for their articles"""
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute("select authors.name, views from authors, \
        (select articles.author as id, count(*) as views from articles, log \
        where articles.slug = split_part(log.path, '/', 3) \
        group by articles.author) as subq \
        where authors.id = subq.id order by views desc")
    print("Authors ordered by popularity: \n")
    for table in cursor.fetchall():
        print("{} -- {} views".format(table[0], table[1]))
    print("\n")
    db.close()


def error_days():
    """Prints all days when more than %1 of site requests failed"""
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute("select err.day, cast(err.errors as float) / req.requests * 100 \
        from err, req \
        where err.day = req.day \
        and cast(err.errors as float) / req.requests > 0.01")
    print("Days where more than 1% of requests failed: \n")
    for table in cursor.fetchall():
        print("{0:s} -- {1:.2f}% errors".format(table[0], table[1]))
    print("\n")
    db.close()


if __name__ == '__main__':
    run()

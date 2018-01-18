import psycopg2

def run():
	top_three_articles()
	top_authors()
	error_days()

# Prints the three most accessed articles in the news database
def top_three_articles():
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

# Prints all authors in order of the number of page views for their articles
def top_authors():
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

# Prints all days when more than %1 of site requests failed
def error_days():
	db = psycopg2.connect("dbname=news")
	cursor = db.cursor()
	cursor.execute("select err.day, cast(err.errors as float) / req.requests * 100 \
		from err, req where err.day = req.day and cast(err.errors as float) / req.requests > 0.01")
	print("Days where more than 1% of requests failed: \n")
	for table in cursor.fetchall():
		print("{0:s} -- {1:.2f}% errors".format(table[0], table[1]))
	print("\n")
	db.close()

if __name__ == '__main__':
	run()

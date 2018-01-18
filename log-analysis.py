import psycopg2

def run():
	top_three_articles()
	#top_authors()
	#error_days()

# Prints the three most accessed articles in the news database
def top_three_articles():
	db = psycopg2.connect("dbname=news")
	cursor = db.cursor()
	cursor.execute("select articles.title, count(*) as views \
		from articles, log where articles.slug = split_part(log.path, '/', 3) \
		group by articles.title order by views desc limit 3")
	print("The top three articles are: \n")
	for table in cursor.fetchall():
		print("{} -- {}".format(table[0], table[1]))
	print("\n")
	db.close()

if __name__ == '__main__':
	run()

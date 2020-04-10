# These are database connectors for the databases jupyter notebook
import sqlite3           # sqlite import
import mysql.connector   # MySQL import
import psycopg2          # postgreSQL import
import pymongo           # MongoDB import

def get_movie_data():
	id_      = None
	title    = 'Jaws'
	year_    = 1975
	duration = 124
	director = 'Steven Spielberg'
	return(id_, title, year_, duration, director)


def sqlite_conn(db):
	try:
		conn = sqlite3.connect(f'data/{db}')   
		#print(f'connected to the {db} database...')
		return(conn)
	except:
		print(f'Error: could not connect to {db} database.')
	

def mysql_conn(db):
	try:
		conn = mysql.connector.connect(host='localhost',
									   user='root',
									   password='testin123!',
									   database=db)
		#print(f'connected to the {db} database...')
		return(conn)
	except:
		print(f'Error: could not connect to {db} database.')


def postgres_conn(db):
	try:
		conn = psycopg2.connect(host='localhost',
								user='postgres',
								password='testin123!',
								database=db)
		#print(f'connected to the {db} database...')
		return(conn)
	except:
		print(f'Error: could not connect to {db} database.')
	
		
def mongo_conn(db):
	try:
		conn = pymongo.MongoClient('localhost', 27017)
		movie_db = conn.movies_db
		#print(f'connected to the {db} database...')
		return(conn, movie_db)
	except:
		print(f'Error: could not connect to {db} database.')

# args for relationals (type, db, conn, cur), args for mongo (type, db, conn)
def close_db(*args):
	type = args[0]
	db = args[1]
	conn = args[2]

	if type == 'mongo':
		conn.close()
		print(f'\n{db} database connection closed.\n')
	else:
		cur = args[3]
		cur.close()
		conn.close()
		print(f'\n{db} database connection closed.\n')
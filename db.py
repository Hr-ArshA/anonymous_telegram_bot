import sqlite3

def create_table():
	connection = sqlite3.connect("anonymous.db")
	cursor = connection.cursor()

	query = """
CREATE TABLE Users(
	user_id varchar(256) NOT NULL UNIQUE, 
	user_hash varchar(256))"""

	cursor.execute(query)
	

def insert(user_id, hash_id):
	try:
		create_table()
	except:
		pass
		
	connection = sqlite3.connect("anonymous.db")
	cursor = connection.cursor()
	
	query = f"""INSERT INTO Users VALUES('{user_id}', '{hash_id}')"""

	cursor.execute(query)
	connection.commit()

	connection.close()

def user_search(user_hash):
	try:
		create_table()
	except:
		pass
		
	connection = sqlite3.connect("anonymous.db")
	cursor = connection.cursor()

	query = f'Select user_id FROM Users WHERE user_hash="{user_hash}"'
	cursor.execute(query)

	data_list = list(cursor)
		
	if data_list != []:
		data = data_list[0][0]
	
		connection.commit()
		connection.close()
	
		return data

def process_table():
	connection = sqlite3.connect("anonymous.db")
	cursor = connection.cursor()

	query = """
CREATE TABLE process(
	sender varchar(256), 
	receiver varchar(256),
	process_hash varchar(256))"""

	cursor.execute(query)
	
def in_process(sender, receiver, process_hash):
	try:
		process_table()
	except:
		pass

	connection = sqlite3.connect("anonymous.db")
	cursor = connection.cursor()

	query = f"""
INSERT INTO process VALUES('{sender}', '{receiver}', '{process_hash}');
"""

	cursor.execute(query)
	connection.commit()

	connection.close()

def process_search(sender):
	try:
		process_table()
	except:
		pass
		
	connection = sqlite3.connect("anonymous.db")
	cursor = connection.cursor()

	query = f'Select receiver FROM process WHERE sender="{sender}"'
	cursor.execute(query)

	data_list = list(cursor)
	print(data_list)
		
	if data_list != []:
		data = data_list[-1][0]
	
		connection.commit()
		connection.close()
	
		return data

def delete_process(user):
	connection = sqlite3.connect("anonymous.db")
	cursor = connection.cursor()
	
	query = f'DELETE FROM process WHERE sender="{user}"'
# '
	cursor.execute(query)
	connection.commit()

	connection.close()


if __name__ == '__main__':
	create_table()
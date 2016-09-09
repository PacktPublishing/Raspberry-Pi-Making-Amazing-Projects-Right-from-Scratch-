import sqlite3

conn = sqlite3.connect('raspi.db')
cursor = conn.cursor()

#Inserting Data
cursor.execute('''
    CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT,
                   	email TEXT unique, password TEXT)
''')
cursor.execute('''INSERT INTO users(name, email, password)
                           VALUES(?,?,?)''', ('Luke', 'luke@skywalker.com', 'iamurfather'))

cursor.execute('''INSERT INTO users(name, email, password)
                           VALUES(?,?,?)''', ('Darth Vader', 'darth@vader.com', 'darkside'))

conn.commit()


#Retrieving Data

user_id = 1
cursor.execute('''SELECT name, email, password FROM users WHERE id=?''', (user_id,))
user1 = cursor.fetchone()
print(user1[0])
allusers = cursor.fetchall()
for row in allusers:
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))



#Deleting or Updating Data

new_email = 'vader@deathstar.com'
userid = 2
cursor.execute('''UPDATE users SET email = ? WHERE id = ? ''', (new_email, userid))

del_userid = 1
cursor.execute('''DELETE FROM users WHERE id = ? ''', (del_userid,))

conn.commit()
conn.close()

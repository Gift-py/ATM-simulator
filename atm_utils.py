import sqlite3

def query_all():
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('SELECT *, oid FROM Accounts')
    records = c.fetchall()

    #commit changes
    conn.commit()
    #close connection
    conn.close()
    return records

def query(oid):
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('SELECT *, oid FROM Accounts WHERE oid='+oid)
    records = c.fetchall()

    #commit changes
    conn.commit()
    #close connection
    conn.close()
    return records

def delete(oid):
    #create db or conect to one
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('DELETE from Accounts WHERE oid= '+ str(oid))
    print('Account deleted successfully')

    #commit changes
    conn.commit()
    #close connection
    conn.close()



# create db
# conn = sqlite3.connect('Bank_Accounts.db')
# create cursor
# c = conn.cursor()

# create table in db
# c.execute('''CREATE TABLE Accounts(
#                Name text,
#                Pin integer,
#                Balance Float
#               )
#          ''')

#commit changes
#conn.commit()
#close connection
#conn.close()
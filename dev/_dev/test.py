# -*- coding: utf8 -*-


from sqlite3 import dbapi2 as sqlite



connection = sqlite.connect('test.db')
connection.row_factory = sqlite.Row
cursor = connection.cursor()


cursor.execute("SELECT * FROM SQLITE_MASTER")
for r in cursor:
    print r
exit()


#cursor.execute("UPDATE katalog SET status_CID=status_CID*1");

#connection.commit()
#cursor.close()

#exit()



cursor.execute('''
    SELECT * FROM katalog
    WHERE status_CID=88 OR status_CID>1 AND status_CID < 11 AND status_CID!=4
 '''); 

i = 0
for row in cursor:
    i+=1
print i




# -*- coding: utf8 -*-

from sqlite3 import dbapi2 as sqlite
import MySQLdb
import re

mys = MySQLdb.connect (host = "localhost",
                       user = "root",
                       passwd = "",
                       db = "ucps")
mysc = mys.cursor()
mysc.execute("SET CHARACTER SET 'utf8'");





lit = sqlite.connect('imported.db')
# def collate_reverse(string1, string2):
#     return -cmp(string1, string2)
# lit.create_collation("suprutf8", collate_reverse)
litc = lit.cursor()


rexps = (
	(re.compile(r"[^\n]* KEY [^\n]*"), ""),
	(re.compile(r" unsigned "), " "),
	(re.compile(r" (NOT )?NULL"), ""),
	(re.compile(r" auto_increment"), " primary key autoincrement"),
	(re.compile(r" (tiny|small)?int\([0-9]*\) "), " integer "),
	(re.compile(r" default( '[^']*')?"), " "),
	(re.compile(r" character set [^ ]* "), " "),
	(re.compile(r" enum([^)]*) "), " varchar(255) "),
	(re.compile(r" on update [^,]*"), ""),
	(re.compile(r" collate utf8_czech_ci"), ""),
	(re.compile(r",[^,)]*\)[^)]*$"), "\n)"),
);


for tbl in ("dopl_char","druhy","katalog_status", "kraje", "zanr","katalog"):
	mysc.execute("SHOW CREATE TABLE `%s`"%tbl);
	cre = mysc.fetchone()[1]
	for rexp in rexps:
		cre = rexp[0].sub(rexp[1], cre)
	
	print "%s" % cre;
	litc.execute(cre)
	print "Table %s was created, starting data import."%tbl;
	
	mys.query("SELECT * FROM `%s`"%tbl);
	res = mys.use_result()
	while 1:
		row = res.fetch_row()
		if not row: break
		row = row[0]
		
		qry = "INSERT INTO `%s` VALUES ('%s')"%( \
			tbl, \
			"','".join([str(item).replace("'","''") for item in row]) \
			);
		litc.execute(qry);



print "deleting...";
litc.execute("DELETE FROM katalog WHERE status_CID*1 not in (1,2,3,4,5,6,7,8,9,88)")


print "setting no data...";
fields = []
mysc.execute("SHOW COLUMNS FROM `katalog`");
for r in mysc.fetchall():
	if r[0] not in ("id", "nazev", "sidlo", "kraj_CID", "druh_CID", "status_CID"):
		fields.append(r[0]);
litc.execute("UPDATE katalog SET %s WHERE status_CID*1 in (1,2,3,4,5,88)" % ','.join(["`"+i+"`=''" for i in fields]) )


print "creating index...";
litc.execute('''
    CREATE INDEX status_CID ON katalog (status_CID)
''');



mysc.close()
mys.close()
litc.close()
lit.commit()
print "ok"

		


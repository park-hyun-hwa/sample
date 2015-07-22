import MySQLdb as mdb
import sys

try:
  con = mdb.connect('localhost','root','tinyos','keti')
  
  cur = con.cursor()
  sql = "SELECT * FROM onenode" 
  cur.execute(sql)
  for i in range(cur.rowcount):
    row = cur.fetchone()
    print row[0]

except mdb.Error,e:
  print "Error"
  sys.exit(1)

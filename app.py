import pymysql

# rds settings
rds_host  = "RDS_ENDPOINT"
admin = "DB_ADMIN"
password = "DB_PASSWORD"

try:
   conn = pymysql.connect(rds_host, user=admin, passwd=password, connect_timeout=5)
except pymysql.MySQLError as e:
   print(e)


IDs = []
with conn.cursor() as cur:
   cur.execute("SHOW PROCESSLIST;")
   for row in cur:
       print(row)
       if row[1] != "event_scheduler" and row[1] != "rdsadmin" and row[1] != admin:
           IDs.append(int(row[0]))
   print(IDs)
   for ID in IDs:
       try:
           cur.execute('CALL mysql.rds_kill('+str(ID)+')')
           conn.commit() 
       except Exception as e:
           print("ID: ",ID)
           print(e)  
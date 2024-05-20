import pymysql.cursors

query = 'select * from docs where sgm_id=207353;'
conn=pymysql.connect(host='history-lab.org', user='de_reader', password='XreadF403', db='declassification_ddrs')
cursor = conn.cursor()
cursor.execute(query)
docs = cursor.fetchall()
print(docs)
cursor.close(),
conn.close()
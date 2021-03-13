import pymysql

db = pymysql.connect(host="192.168.2.7", port=4000, user="maxuser", passwd="maxpwd")
cursor = db.cursor()

print('The last 10 rows of zipcodes_one are:')
cursor.execute("SELECT * FROM zipcodes_one.zipcodes_one LIMIT 9990,10;")
results = cursor.fetchall()
for result in results:
    print(result)

print('The first 10 rows of zipcodes_two are:')
cursor.execute("SELECT * FROM zipcodes_two.zipcodes_two LIMIT 10")
results = cursor.fetchall()
for result in results:
    print(result)

print('The largest zipcode number in zipcodes_one is:')
cursor = db.cursor()
cursor.execute("SELECT Zipcode FROM zipcodes_one.zipcodes_one ORDER BY Zipcode DESC LIMIT 1;")
results = cursor.fetchall()
for result in results:
    print(result)

print('The smallest zipcode number in zipcodes_two is:')
cursor = db.cursor()
cursor.execute("SELECT Zipcode FROM zipcodes_two.zipcodes_two ORDER BY Zipcode ASC LIMIT 1")
results = cursor.fetchall()
for result in results:
    print(result)

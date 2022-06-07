from flask import Flask
import mysql.connector

mydb = mysql.connector.connect(
  host="10.0.50.252",
  user="OKEDBADmin",
  password='YOURPASSWORDHERE',
  database="UPDatabase",
  auth_plugin='mysql_native_password'
) 

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Table01")
dbResult = mycursor.fetchone()
print('MySQLDB Data: ')
print(dbResult)
 
  
app = Flask(__name__)

count = 0
@app.route('/')
def index():
    global count
    count += 1
    return 'Hello from application ' + str(count)
    #return 'Goodbye from application ' + str(count)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
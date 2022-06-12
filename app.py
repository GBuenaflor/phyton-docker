
from flask import Flask
import mysql.connector
  mydb = mysql.connector.connect(
    host="10.0.50.252",
    user="OKEDBADminPOC",
    password='noP33swOrDinthi$$',
    database="UPDatabase",
    port=3306
   # auth_plugin='mysql_native_password'
  ) 
   mycursor = mydb.cursor()
   mycursor.execute("SELECT user FROM Table01 WHERE ID = 1;")
   dbResult = mycursor.fetchone()
   print('MySQLDB Data: ')
   print(dbResult)
    
app = Flask(__name__)
count = 0

@app.route('/')
def index():
    global count
    count += 1           
    return 'Python with Flask Website OKE,MySQL,Terraform,DevOPS. GBuenaflor/iSRAel : ' + str(count) + dbResult

if __name__ == '__main__':
    app.run(host='0.0.0.0')

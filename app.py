# Python Flask build_spec.yaml 
# POC Develop By GB Buenaflor and isRAEL Casisdsid
# OKE , MySQL ,Terraform ,DevOPS

from flask import Flask
app = Flask(__name__)

count = 0

@app.route('/')
def index():
    global count
    count += 1
    return 'Python with Flask Website - Cloud, OKE, MySQL, Terraform, DevOPS - 27June2022:     ' + str(count) 

if __name__ == '__main__':
    app.run(host='0.0.0.0')

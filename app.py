from flask import Flask
app = Flask(__name__)

count = 0

@app.route('/')
def index():
    global count
    count += 1
    return 'Python with Flask Website \n
     Technology : OKE,MySQL,Terraform,DevOps \n
     Develop by : GBuenaflor/iSRAel \n
     Count      : ' + str(count) 

if __name__ == '__main__':
    app.run(host='0.0.0.0')

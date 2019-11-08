from flask import Flask,jsonify,request

app=Flask(__name__)


@app.route('/hello')
def hello():
    return "Hello"


@app.route('/add',methods=['POST','GET'])
def add_nos():
    dataDict=request.get_json()
    x=dataDict['x']
    y=dataDict['y']
    z=x+y
    retJson={
        'z':z
    }
    return jsonify(retJson)





















if __name__ == '__main__':
    app.run(debug=True)

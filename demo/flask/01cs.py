from flask import Flask,request,render_template,jsonify
import db
import multiprocessing
# from flask.logging import default_handler
import logging

# app = Flask(__name__,root_path='./')
app = Flask(__name__, template_folder='./',static_folder="",static_url_path="")
# app.logger.removeHandler(default_handler)

@app.route('/')
def hello():
    return 'Hello, World!333344'

    # message=db.get_data()
    # # for i in  message:
    # #     print(i)
    # return jsonify(message)

@app.route('/json')
def hello2():
    message=db.get_data()
    # for i in  message:
    #     print(i)
    return jsonify(message)

# @app.route('/test',methods=['POST','GET'])
# def test():
#     pass
#     if request.method=="GET":
#         print("GET")
#         return render_template('test.html',message="GET")
#     else:
#         print('POST')
#         id=request.form['ID']
#         # message=db.get_data(id)
#         message=db.get_data()
#         # for i in  message:
#         #     print(i)
#         return render_template('test.html',message=message,id=id)
#

@app.route('/d', methods=["GET"])
def d222():
    return render_template('d.html')

if __name__ == '__main__':
    app.run(debug=True)
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run()

def foo():
    app.run()

def run():
    p = multiprocessing.Process(target=foo)
    p.start()

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient 
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:JEix6NjqkUe2HlnI@cluster0.dx5eieg.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket2.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    doc = {
        'num': count,
        'bucket' : bucket_receive,
        'done' : 0
    }
    db.bucket2.insert_one(doc)
    
    return jsonify({'msg': '저장 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '완료!'})

@app.route("/bucket/undo", methods=["POST"])
def bucket_undo():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})

    return jsonify({'msg': '취소!'})
    
@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket2.find({},{'_id':False}))
    return jsonify({'result' : all_buckets })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
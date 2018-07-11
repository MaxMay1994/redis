from flask import Flask
from flask import request
import redis

r_server = redis.Redis('localhost')
r_server.set('user:next', '1')

app = Flask(__name__)


@app.route('/')
def index():
    return 'INDEX'


@app.route('/users', methods=['GET'])
def getUsers():
        return r_server.get('user')

@app.route('/users/<string:id>', methods=['GET'])
def getUsersId(id):
        return r_server.get('user:'+id)


@app.route('/users', methods=['POST'])
def postUsers():
        userName = request.form['name']
        userKey = 'user:' + r_server.get('user:next').decode('utf-8')
        r_server.set(userKey, userName)
        r_server.incr('user:next')
        return userName


if __name__ == '__main__':
    app.run()

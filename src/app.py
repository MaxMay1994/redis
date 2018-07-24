from flask import Flask
from flask import request
from flask import jsonify
import redis

r_server = redis.Redis('localhost')
r_server.set('actors:next', '1')
r_server.set('directors:next', '1')
r_server.set('movies:next', '1')
r_server.set('roles:next', '1')

app = Flask(__name__)


@app.route('/')
def index():
    return 'INDEX'


@app.route('/actors/<string:id>', methods=['GET'])
def getActor(id):
        return jsonify({'firstName': r_server.hget('actors:'+id, 'firstName').decode("utf-8"),
                        'lastName': r_server.hget('actors:'+id, 'lastName').decode("utf-8"),
                        'gender': r_server.hget('actors:'+id, 'gender').decode("utf-8")})


@app.route('/directors/<string:id>', methods=['GET'])
def getDirectors(id):
        return jsonify({'firstName': r_server.hget('directors:'+id, 'firstName').decode("utf-8"),
                        'lastName': r_server.hget('directors:'+id, 'lastName').decode("utf-8")})


@app.route('/movies/<string:id>', methods=['GET'])
def getMovies(id):
    return jsonify({'name': r_server.hget('movies:' + id, 'name').decode("utf-8"),
                    'year': r_server.hget('movies:' + id, 'year').decode("utf-8"),
                    'rank': r_server.hget('movies:' + id, 'rank').decode("utf-8")})


@app.route('/roles/<string:id>', methods=['GET'])
def getRoles(id):
    return jsonify({'actor_id': r_server.hget('roles:' + id, 'actor_id').decode("utf-8"),
                    'movie_id': r_server.hget('roles:' + id, 'movie_id').decode("utf-8"),
                    'role': r_server.hget('roles:' + id, 'rank').decode("utf-8")})


@app.route('/actors', methods=['POST'])
def postActors():
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        gender = request.form['gender']
        actorsKey = 'actors:' + r_server.get('actors:next').decode('utf-8')
        list = {'firstName': firstName, 'lastName': lastName, 'gender': gender}
        r_server.hmset(actorsKey, list)
        r_server.incr('actors:next')
        return actorsKey


@app.route('/directors', methods=['POST'])
def postDirectors():
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        directorsKey = 'directors:' + r_server.get('directors:next').decode('utf-8')
        list = {'firstName': firstName, 'lastName': lastName}
        r_server.hmset(directorsKey, list)
        r_server.incr('direcotors:next')
        return directorsKey


@app.route('/movies', methods=['POST'])
def postMovies():
        name = request.form['name']
        year = request.form['year']
        rank = request.form['rank']
        movieKey = 'movies:' + r_server.get('movies:next').decode('utf-8')
        list = {'name': name, 'year': year, 'rank': rank}
        r_server.hmset(movieKey, list)
        r_server.incr('movies:next')
        return movieKey


@app.route('/roles', methods=['POST'])
def post_roles():
    actor_id = request.form['actor_id']
    movie_id = request.form['movie_id']
    role = request.form['role']
    role_key = 'roles:' + r_server.get('roles:next').decode('utf-8')
    role_list = {'actorId': actor_id, 'movieId': movie_id, 'role': role}
    r_server.hmset(role_key, role_list)
    r_server.incr('roles:next')
    return role_key


if __name__ == '__main__':
    app.run()

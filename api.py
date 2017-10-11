from flask import Flask, request, jsonify, abort
from redis import Redis, RedisError
import os
import socket
import json
import random

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
print( 'Redis host:', redis_host)
redis = Redis(host=redis_host, db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    return """
    /quotes POST with { "quote": "Educative statement", "tags": [ "GraphQL"]}
    /quotes GET  ?tag=rest
    /quotes/id GET
    /quotes/random GET
    /quotes/id/tags   { "tags": ["REST"]}

    /tags GET
    /tags POST    { "tags": ["REST"]}


    """

@app.route("/quotes", methods=["POST"])
def add_quote():
    j = request.get_json(force=True)
    cleaned = {}
    if not "quote" in j:
        return "no quote in JSON body", 400
    cleaned['quote'] = j['quote']
    if "tags" in j:
        add_t(j["tags"])
        cleaned['tags'] = j["tags"]   

    id = redis.incr('quote_id_counter')         
    cleaned['id'] = id
    add_q(cleaned)

    return jsonify(cleaned)


@app.route("/quotes/random", methods=["GET"])
def random_quote():
    return jsonify(get_q(get_random=True))

@app.route("/quotes", methods=["GET"])
def list_quotes():
    return jsonify(get_q())


@app.route("/quotes/<int:id>", methods=["GET"])
def get_quote(id):
    return jsonify(get_q(id))


@app.route("/quotes/clear")
def clear_quotes():
    redis.delete('quotes')


def get_q(id=None, get_random=False):
    try:
        s = redis.get('quotes')
        if s:
            s = s.decode('utf-8')
    except RedisError:
        if id or get_random: 
            abort(404)
        else:
             return []
    quotes = json.loads(s)
    print( quotes )
    if id:
        for q in quotes:
            if q["id"] == id: 
                return q
        abort(404)
    if get_random:
        return random.choice(quotes)

    return quotes

def add_q(q):
    s = '[]'
    try:
        s = redis.get('quotes')
        if s:
            s = s.decode('utf-8')
        else:
            s = '[]'
    except RedisError:
        pass
    quotes = json.loads(s)
    quotes.append(q)
    redis.set('quotes', json.dumps(quotes))


@app.route("/tags", methods=["GET"])
def list_tags():
    return jsonify(get_t())

@app.route("/tags", methods=["POST"])
def add_tags():
    # new tags from post body
    return jsonify(add_t())



def get_t(get_random=False):
    s = '[]'
    try:
        t = redis.get('tags')
        if t:
            s = t.decode('utf-8')
    except RedisError:
        pass
    tags = json.loads(s)
    if get_random:
        return random.choice(tags)
    return tags

def add_t(tags):
    old_tags = []
    try:
        s = redis.get('tags')
        if s:
            old_tags = json.loads(s.decode('utf-8'))
    except RedisError:
        pass

    added = []
    for t in tags:
        if t not in old_tags:
            added.append(t)
            old_tags.append(t)
    redis.set('tags', json.dumps(old_tags))
    return added




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8042)


from datetime import datetime
from flask import Flask, request
from mongokit import Connection

from models import Translation, User
from translate import google_translate

import uuid

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])
connection.register([Translation, User])

@app.route('/<string:source>/<string:target>/<string:key>')
def translate(source, target, key):
    query = request.args['query']

    users = connection.gtproxy.users
    user = users.User.find_one({'key': key})
    if user is None:
        return "Forbidden", 503

    print user

    translations  = connection.gtproxy.translations
    search_dict = {
        'source': source,
        'target': target,
        'query':  query,
        'author': user.username
    }
    now = datetime.now()
    result = translations.Translation.find_one(search_dict)
    if result is None:
        result = google_translate(query, source, target)
        if result is None:
            return 'Invalid query', 200
        result = translations.Translation(dict(search_dict, 
                                               response=result,
                                               created=now,
                                               last_used=now,
                                               query_count=0))
    result.last_used = now
    result.query_count += 1
    result.save()

    user.query_count += 1
    user.save()

    return result['response'], 200

def create_user(username):
    users = connection.gtproxy.users
    key = unicode(uuid.uuid4().hex)
    user = users.User({'username': unicode(username), 
                       'key': key,
                       'created': datetime.now(),
                       'query_count': 0})
    user.save()
    return key
    
if __name__ == '__main__':
    app.debug = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run()

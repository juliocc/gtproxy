from flask import Flask, request
from mongokit import Connection

from models import Translation
from translate import google_translate

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])
connection.register([Translation])

@app.route('/<string:source>/<string:target>')
def translate(source, target):
    query = request.args['query']
    collection  = connection['gtproxy'].translations
    search_dict = {
        'source': source,
        'target': target,
        'query':  query,
    }
    result = collection.Translation.find_one(search_dict)
    if result is None:
        result = google_translate(query, source, target)
        if result is None:
            return 'Invalid query', 200
        result = collection.Translation(dict(search_dict, response=result))
        result.save()
    return result['response'], 200

if __name__ == '__main__':
    app.debug = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run()

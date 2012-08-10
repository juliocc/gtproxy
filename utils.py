import uuid
import cPickle
from datetime import datetime

def force_unicode(s):
    if isinstance(s, str):
        return unicode(s, "utf-8")
    elif isinstance(s, unicode):
        return s
    else:
        raise Exception('WTF?')

def import_pickle(connection, source, target, filename):
    translations  = connection.gtproxy.translations
    source = unicode(source)
    target = unicode(target)
    with open(filename) as f:
        d = cPickle.load(f)
        for word, definition in d.iteritems():
            now = datetime.now()
            word = force_unicode(word.strip())
            definition = force_unicode(definition.strip())
            if word.find('//tco/') != -1:
                continue
            if not word or not definition:
                continue
            # print source,"|", target,"|",  type(word),"|",  type(definition)
            # print u"[{}->{}] '{}': '{}'".format(source, target, word, definition)
            params = {
                'source': source,
                'target': target,
                'query':  word,
                'response': definition,
                'author': u'__system__',
                'created': now,
                'last_used': now,
                'query_count': 0                
            }
            t = translations.Translation(params)
            t.save()

def import_pickles(connection):
    import_pickle(connection, 'en', 'es', 'palabras.pickle')
    import_pickle(connection, 'es', 'en', 'words.pickle')

def create_user(connection, username):
    users = connection.gtproxy.users
    key = unicode(uuid.uuid4().hex)
    user = users.User({'username': unicode(username), 
                       'key': key,
                       'created': datetime.now(),
                       'query_count': 0})
    user.save()
    return key

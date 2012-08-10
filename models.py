import datetime
from mongokit import Document

def length_exact(length):
    def validate(value):
        if len(value) == length:
            return True
        raise Exception('%s must be exactly %s characters long' % (value, length))
    return validate

def min_length(length):
    def validate(value):
        if len(value) >= length:
            return True
        raise Exception('%s must be more than %s characters long' % (value, length))
    return validate

class User(Document):
    structure = {
        'username'    : unicode,
        'key'         : unicode,
        'query_count' : int,
        'created'     : datetime.datetime
    }

    indexes = [
        {
            'fields': 'username',
            'unique': True
        },
        {
            'fields': 'key',
            'unique': True
        },
    ]

    validators = {
        'key': length_exact(32), # uuid4.hex len
    }

    use_dot_notation = True

    def __repr__(self):
        return '<User %s>' % (self.username)
    

class Translation(Document):
    structure = {
        'source'      : unicode,
        'target'      : unicode,
        'query'       : unicode,
        'response'    : unicode,
        'author'      : unicode,
        'created'     : datetime.datetime,
        'last_used'   : datetime.datetime,
        'query_count' : int
    }
    indexes = [
        {
            'fields': ['source', 'target', 'query'],
            'unique': True
        },
    ]
    validators = {
        'source': length_exact(2),
        'target': length_exact(2),
        'query':  min_length(1),
    }
    use_dot_notation = True
    def __repr__(self):
        return '<Translation (%s-%s) %s>' % (self.source, self.target,
                                             self.response)

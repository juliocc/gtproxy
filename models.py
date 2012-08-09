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

class Translation(Document):
    structure = {
        'source'   : unicode,
        'target'   : unicode,
        'query'    : unicode,
        'response' : unicode,
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

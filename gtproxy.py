import os
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
import urllib2
import json
import urllib

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Cache(Base):
    __tablename__ = "cache"
    
    id = Column(Integer, primary_key=True)
    source = Column(String(2))  
    target = Column(String(2))
    question = Column(String)
    result = Column(String)


def create_tables():
    Base.metadata.create_all(engine)


def translate(q,source,target):
    key = 'AIzaSyCgl2cikF18bXZO5MmzQdGq1z5EZjNZ6M8'
    url = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=%s&target=%s'%(key,urllib.quote(q),source,target)
    print url
    done = False;
    while not done:
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            done = True
        except:
            print 'error accessing url';

    results = json.load(response)
    result = results['data']['translations'][0]['translatedText']
    return result
    
class GTProxy(object):

    def __init__(self):
        self.querys = 0;

    def dispatch_request(self, request):
        source = request.args.get('source','')
        target = request.args.get('target','')
        print source,target
        q = request.args.get('q','');
        if source!='' and target!='' and q!='':
            if source=='es' and target=='en':
                self.querys = self.querys + 1
                try:
                    result = words[q] 
                except:
                    result = translate(q,source,target);
                    words[q] = result
            elif source=='en' and target=='es':
                self.querys = self.querys + 1
                try:
                    result = palabras[q] 
                except:
                    result = translate(q,source,target);
                    palabras[q] = result
            else:
                result = translate(q,source,target);
        else: 
            result = ''

        if self.querys > 100:
            with open('words.pickle','w') as f:
                cPickle.dump(words,f)
            with open('palabras.pickle','w') as f:
                cPickle.dump(palabras,f)
            self.querys = 0;




        return Response(result)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app():
    app = GTProxy()
    return app

if __name__ == '__main__':
    # create_tables()

    global words;
    try:
        with open('words.pickle') as f:
            words = cPickle.load(f)
    except:
        words = {}

    global palabras;
    try:
        with open('palabras.pickle') as f:
            palabras = cPickle.load(f)
    except:
        palabras = {}

    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)



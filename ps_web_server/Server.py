import cherrypy
import os


class HelloWorld(object):
    def __init__(self):
        self.number = 0

    def index(self):
        self.number += 1
        return index
    index.exposed = True

cherrypy.quickstart(HelloWorld())
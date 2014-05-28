import cherrypy
import os, os.path
from ps_web_server.Wrapper import Wrapper, MockWrapper


class HelloWorld(object):
    def __init__(self):
        self._wrapper = MockWrapper()
        self._wrapper.connect()

    @cherrypy.expose
    def index(self):
        index_file_path = os.path.join(os.path.dirname(__file__), 'index.html')
        with open(index_file_path)as f:
            index = f.read()
        return index

    @cherrypy.expose
    def get_current_values(self):
        json_current_values = self._wrapper.get_current_json()
        return json_current_values

    @cherrypy.expose
    def get_all_values(self):
        json_all_values = self._wrapper.get_all_json()
        return json_all_values

    @cherrypy.expose
    def set_target_voltage(self, voltage):
        try:
            self._wrapper.set_voltage(int(voltage))
        except Exception:
            pass

    @cherrypy.expose
    def set_target_current(self, current):
        try:
            self._wrapper.set_current(float(current))
        except Exception:
            pass

    @cherrypy.expose
    def turn_on(self):
        self._wrapper.set_device_on()

    @cherrypy.expose
    def turn_off(self):
        self._wrapper.set_device_off()


pat = os.path.abspath(os.getcwd())
conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './css'
    },
    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './js'
    }
}

cherrypy.quickstart(HelloWorld(), '/', conf)
import cherrypy
import os
from ps_web_server.PsWebWrapper import Wrapper, MockWrapper
import json


class PsWebServer(object):
    def __init__(self):
        self._wrapper = Wrapper()
        self._wrapper.connect()

    @cherrypy.expose
    def index(self):
        self._wrapper.connect()
        index_file_path = os.path.join(os.path.dirname(__file__), 'index.html')
        with open(index_file_path)as f:
            index = f.read()
        return index

    @cherrypy.expose
    def get_values(self):
        try:
            json_current_values = self._wrapper.get_current_json()
            return json_current_values
        except Exception as e:
            return ""

    @cherrypy.expose
    def set_target_voltage(self, voltage):
        try:
            self._wrapper.set_voltage(float(voltage))
        except Exception:
            pass

    @cherrypy.expose
    def set_target_current(self, current):
        try:
            self._wrapper.set_current(int(current))
        except Exception:
            pass

    @cherrypy.expose
    def turn_on(self):
        try:
            self._wrapper.set_device_on()
        except:
            pass

    @cherrypy.expose
    def turn_off(self):
        try:
            self._wrapper.set_device_off()
        except:
            pass

    @cherrypy.expose
    def connected(self):
        try:
            return json.dumps(self._wrapper.connected())
        except:
            pass


conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.split(__file__)[0]
    },
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './css'
    },
    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './js'
    },
    '/fonts': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './fonts'
    }
}


def run():
    cherrypy.quickstart(PsWebServer(), '/', conf)


if __name__ == "__main__":
    run()
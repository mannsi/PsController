import cherrypy
import os
from ps_web_server.PsWebWrapper import Wrapper, MockWrapper
import json

# TODO Test connect disconnect when website is running
# TODO Test using relative paths in javascript. /get_all_values and not localhost:8080/get_all_values
# TODO Document-a web API fyrir device. Þannig get ég kannski bara gleymt python kóða integration !
# TODO Check if installing still works
# TODO búa til leiðbeiningar fyrir Frissa svo hann geti sett þetta upp með website


class PsWebServer(object):
    def __init__(self):
        self._wrapper = Wrapper()
        self._wrapper.connect()
        if self._wrapper.connected():
            self._wrapper.start_streaming()

    @cherrypy.expose
    def index(self):
        self._wrapper.connect()
        if self._wrapper.connected():
            self._wrapper.start_streaming()
        index_file_path = os.path.join(os.path.dirname(__file__), 'index.html')
        with open(index_file_path)as f:
            index = f.read()
        return index

    @cherrypy.expose
    def get_current_values(self):
        try:
            json_current_values = self._wrapper.get_current_json()
            return json_current_values
        except:
            return ""

    @cherrypy.expose
    def get_all_values(self):
        try:
            json_all_values = self._wrapper.get_all_json()
            return json_all_values
        except:
            return ""

    @cherrypy.expose
    def set_target_voltage(self, voltage):
        try:
            self._wrapper.set_voltage(int(voltage))
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
        'tools.staticdir.root': os.path.abspath(os.getcwd())
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
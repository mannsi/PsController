import cherrypy
import os
from ps_web_server.Wrapper import Wrapper, MockWrapper
import json

# TODO prófa að blokka UI þegar ekki tekst að tengjast og fara þá að polla device um tengingu á 1 sec fresti
# TODO Stress testa. Ákveða hvað á að gerast þegar shit hits the fans. Þá blokkar UI
# TODO Document-a web API fyrir device. Þannig get ég kannski bara gleymt python kóða integration !
# TODO búa til leiðbeiningar fyrir Frissa svo hann geti sett þetta upp með website


class HelloWorld(object):
    def __init__(self):
        self._wrapper = Wrapper()
        self._wrapper.connect()
        if self._wrapper.connected():
            self._wrapper.start_streaming()

    @cherrypy.expose
    def index(self):
        if self._wrapper.connected():
            file_to_show = 'index.html'
        else:
            file_to_show = 'NoDeviceFound.html'

        index_file_path = os.path.join(os.path.dirname(__file__), file_to_show)
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
    },
    '/fonts': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './fonts'
    }
}

cherrypy.quickstart(HelloWorld(), '/', conf)
import cherrypy
import os
from ps_web_server.PsWebWrapper import Wrapper, MockWrapper
import json
import signal
import sys

host = '127.0.0.1'
port = 8080


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
    def all_values(self):
        """
        Gets all values of the device as JSON dict.
        :returns:
            "outputVoltage_V"
            "outputCurrent_mA"
            "inputVoltage_V"
            "targetVoltage_V"
            "targetCurrent_mA"
            "outputOn"
            "connected"
        """
        try:
            json_current_values = self._wrapper.get_all_values_json()
            return json_current_values
        except Exception as e:
            return ""

    @cherrypy.expose
    def voltage(self, **params):
        """
        Gets or sets the voltage of the device. Values are in V
        :param params: 'voltage' [V]
        """
        try:
            if cherrypy.request.method == 'GET':
                return self._wrapper.get_voltage()
            elif cherrypy.request.method == 'POST':
                if 'voltage' in cherrypy.request.body_params:
                    self._wrapper.set_voltage(float(cherrypy.request.body_params['voltage']))
        except Exception:
            pass

    @cherrypy.expose
    def current(self, **params):
        """
        Gets or sets the current of the device. Values are in mA
        :param params: 'current' [mA]
        """
        try:
            if cherrypy.request.method == 'GET':
                return self._wrapper.get_current()
            elif cherrypy.request.method == 'POST':
                if 'current' in cherrypy.request.body_params:
                    self._wrapper.set_current(int(cherrypy.request.body_params['current']))
        except Exception:
            pass

    @cherrypy.expose
    def output_on(self, **params):
        """
        Gets or sets the 'on' value of the device
        :param params: 'value' [1, 0]
        :return:
        """
        try:
            if cherrypy.request.method == 'GET':
                return self._wrapper.connected()
            elif cherrypy.request.method == 'POST':
                if 'value' in cherrypy.request.body_params and cherrypy.request.body_params['value'] == "1":
                    self._wrapper.set_device_on()
                else:
                    self._wrapper.set_device_off()
        except:
            pass

    @cherrypy.expose
    def device_connected(self):
        try:
            return json.dumps(self._wrapper.connected())
        except:
            pass


# Catch the Ctrl-C interrupt and shut down the cherrypy server
def signal_handler(signal, frame):
    cherrypy.engine.exit()
    sys.exit(0)


signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def run():
    conf = {
        'global': {
            'server.socket_host': host,
            'server.socket_port': port
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.path.split(__file__)[0])
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

    cherrypy.quickstart(PsWebServer(), '/', conf)


if __name__ == "__main__":
    run()
import cherrypy
import os
from ps_web_server.PsWebWrapper import Wrapper


class PsWebServer(object):
    def __init__(self, port, ps_log_level, server_logging, resources_base_dir=None):
        self._host = '127.0.0.1'
        self._port = port
        self.server_logging = server_logging
        self._wrapper = Wrapper(ps_log_level)
        self.resources_base_dir = resources_base_dir or os.path.abspath(os.path.split(__file__)[0])

    def start(self, resources_base_dir=None):
        """Starts the web server
        :return: None
        """

        conf = {
            'global': {
                'server.socket_host': self._host,
                'server.socket_port': self._port
            },
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': self.resources_base_dir
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

        self._wrapper.connect()

        if not self.server_logging:
            cherrypy.log.screen = None
        cherrypy.quickstart(self, '/', conf)

    @cherrypy.expose
    def stop(self):
        """Stops the web server

        :return: None
        """
        cherrypy.engine.exit()

    @cherrypy.expose
    def index(self):
        """Gives the default index page of the web server

        :return: str -- Index page of web server
        """
        self._wrapper.connect()
        index_file_path = os.path.join(self.resources_base_dir, 'index.html')
        with open(index_file_path)as f:
            index = f.read()
        return index

    @cherrypy.expose
    def all_values(self):
        """Gets all values of the device.

        :return: str -- JSON dict with the following keys::
            - output_voltage_V
            - output_current_mA
            - target_voltage_V
            - current_limit_mA
            - output_on
            - connected
            - authentication_error

        """
        return self._wrapper.get_all_values_json()


    @cherrypy.expose
    def voltage(self, **params):
        """Gets or sets the voltage of the device. Pass in target voltage with key 'target_voltage_V' to set the voltage value

        :param params: Dictionary of values. Value with key 'target_voltage_V' will be used if provided
        :type params: dict
        :return: str or None -- If called with no parameter then output voltage is returned in units of V

        """
        if 'target_voltage_V' in params:
            self._wrapper.set_voltage(float(params['target_voltage_V']))
        else:
            return self._wrapper.get_voltage()

    @cherrypy.expose
    def current(self, **params):
        """ Gets or sets the current of the device. Pass in target current with key 'current_limit_mA' to set the voltage value

        :param params: Value with key 'current_limit_mA' will be used if provided
        :type params: dict
        :return: str or None -- If called with no parameter then output current is returned in units of mA

        """
        if 'current_limit_mA' in params:
            self._wrapper.set_current(int(params['current_limit_mA']))
        else:
            return self._wrapper.get_current()

    @cherrypy.expose
    def output_on(self, **params):
        """ Gets or set the output on value of the device. Pass in value "0" or "1" on key 'on' to set the output value

        :param params: Value with key 'on' will be used if provided
        :type params: dict
        :return: str or None -- Returns values "0" or "1" if called with no parameter
        """
        if 'on' in params:
            if params['on'] == "1":
                self._wrapper.set_device_on()
            else:
                self._wrapper.set_device_off()
        else:
            return "1" if self._wrapper.get_output_on() else "0"






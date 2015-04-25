import ps_web_server.PsWebServer
import argparse
import logging
from ps_controller import __version__


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='Port that server should listen on. Default is 8080', type=int)
parser.add_argument('-v', '--version', help='Software version', action='store_true')
parser.add_argument('-d', '--debug', help='Receive debug message from PsController', action='store_true')
parser.add_argument('-dw', '--debugWebServer', help='Receive debug message from web server', action='store_true')

args = parser.parse_args()


def run():
    if args.version:
        print(__version__)
        return

    ps_log_level = logging.ERROR
    web_server_debugging = False
    port = 8080

    if args.debug:
        ps_log_level = logging.DEBUG

    if args.debugWebServer:
        web_server_debugging = True

    if args.port:
        print(args.port)
        port = args.port

    server = ps_web_server.PsWebServer.PsWebServer(port, ps_log_level, web_server_debugging)

    server.start()


if __name__ == "__main__":
    run()
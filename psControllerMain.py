import ps_web_server.PsWebServer as webServer
import argparse
from ps_controller import __version__


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='Port that server should listen on. Default is 8080', type=int)
parser.add_argument('-v', '--version', help='Software version', action='store_true')
parser.add_argument('-d', '--debug', help='Run debug trace', action='store_true')

args = parser.parse_args()


def run():
    if args.version:
        print(__version__)
        return

    if args.port:
        print(args.port)
        webServer.port = args.port

    if args.debug:
        webServer.set_debug()

    webServer.run()


if __name__ == "__main__":
    run()
import ps_web_server.PsWebServer as webServer
import argparse
from ps_controller import __version__

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='Port that server should listen on. Default is 8080')
parser.add_argument('-v', '--version', help='Software version', action='store_true')
args = parser.parse_args()
if args.port:
    print(args.port)
    webServer.port = int(args.port)


def run():
    if args.version:
        print(__version__)
        return
    print(webServer.port)
    webServer.run()


if __name__ == "__main__":
    run()
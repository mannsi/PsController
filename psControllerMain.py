import ps_web_server.PsWebServer as webServer
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='Port that server should listen on. Default is 8080')
args = parser.parse_args()
if args.port:
    print(args.port)
    webServer.port = int(args.port)


def run():
    print(webServer.port)
    webServer.run()


if __name__ == "__main__":
    run()
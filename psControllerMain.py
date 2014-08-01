import ps_web_server.PsWebServer as webServer
import argparse
import os


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?', help='[start, stop, status]')
    args = parser.parse_args()
    if args.command == 'start' or not args.command:
        webServer.run()
    elif args.command == 'stop':
        pass
    elif args.command == 'status':
        pass

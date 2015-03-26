#!/usr/bin/env python

import argparse
import SocketServer
import socket

lhost, lport = "", 5353
fhost, fport = "", 53

def encrypt(data):
    char_encrypt = lambda x: 31 - x if x < 32 else \
                             x if x == 32 else \
                             159 - x if x < 127 else \
                             127 if x == 127 else \
                             383 - x
    return ''.join([chr(char_encrypt(ord(ch))) for ch in data])

class UdpHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'Got a request.'
        data = self.request[0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(encrypt(data), (fhost, fport))
        print 'Forwarded the request.'
        try:
            response = sock.recv(1024)
            print 'Got a response.'
        except socket.timeout:
            print 'Response timeout. Ignored.'
            return

        self.request[1].sendto(encrypt(response), self.client_address)
        print 'Sent response back.'

def main():
    global lhost, lport, fhost, fport

    parser = argparse.ArgumentParser(
        description='UDP Forwarder.')

    parser.add_argument(
        'laddr', metavar='listen-address[:listen-port]',
        help='The address and port to listen to. The port defaults to {}.'.format(lport))
    parser.add_argument(
        'faddr', metavar='forward-address[:forward-port]',
        help='The address and port to forward the datagrams to. The port defaults to {}.'.format(fport))

    args = parser.parse_args()

    if ':' in args.laddr:
        lhost, lport = args.laddr.split(':')
        lport = int(lport)
    else:
        lhost = args.laddr

    if ':' in args.faddr:
        fhost, fport = args.faddr.split(':')
        fport = int(fport)
    else:
        fhost = args.faddr

    server = SocketServer.UDPServer((lhost, lport), UdpHandler)
    try:
        print 'Listening...'
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print 'Error:', e

if __name__ == '__main__':
    main()

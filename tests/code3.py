import sys
import os
import hashlib

from twisted.internet.protocol import ServerFactory, ProcessProtocol
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor, threads

class TailProtocol(ProcessProtocol):
    def __init__(self, write_callback):
        self.write = write_callback

    def outReceived(self, data):
        self.write("Begin lastlog\n")
        data = [line for line in data.split('\n') if not line.startswith('==')]
        for d in data:
            self.write(d + '\n')
        self.write("End lastlog\n")

    def processEnded(self, reason):
        if reason.value.exitCode != 0:
            log.msg(reason)

class HashCompute(object):
    def __init__(self, path, write_callback):
        self.path = path
        self.write = write_callback

    def blockingMethod(self):
        os.path.isfile(self.path)
        data = file(self.path).read()
        # uncomment to add more delay
        # import time
        # time.sleep(10)
        return hashlib.sha1(data).hexdigest()

    def compute(self):
        d = threads.deferToThread(self.blockingMethod)
        d.addCallback(self.ret)
        d.addErrback(self.err)

    def ret(self, hdata):
        self.write("File hash is : %s\n" % hdata)

    def err(self, failure):
        self.write("An error occured : %s\n" % failure.getErrorMessage())

class CmdProtocol(LineReceiver):

    delimiter = '\n'

    def processCmd(self, line):
        if line.startswith('lastlog'):
            tailProtocol = TailProtocol(self.transport.write)
            reactor.spawnProcess(tailProtocol, '/usr/bin/tail', args=['/usr/bin/tail', '-10', '/var/log/syslog'])
        elif line.startswith('comphash'):
            try:
                useless, path = line.split(' ')
            except:
                self.transport.write('Please provide a path.\n')
                return
            hc = HashCompute(path, self.transport.write)
            hc.compute()
        elif line.startswith('exit'):
            self.transport.loseConnection()
        else:
            self.transport.write('Command not found.\n')

    def connectionMade(self):
        self.client_ip = self.transport.getPeer()[1]
        log.msg("Client connection from %s" % self.client_ip)
        if len(self.factory.clients) >= self.factory.clients_max:
            log.msg("Too many connections. bye !")
            self.client_ip = None
            self.transport.loseConnection()
        else:
            self.factory.clients.append(self.client_ip)

    def connectionLost(self, reason):
        log.msg('Lost client connection.  Reason: %s' % reason)
        if self.client_ip:
            self.factory.clients.remove(self.client_ip)

    def lineReceived(self, line):
        log.msg('Cmd received from %s : %s' % (self.client_ip, line))
        self.processCmd(line)

class MyFactory(ServerFactory):

    protocol = CmdProtocol

    def __init__(self, clients_max=10):
        self.clients_max = clients_max
        self.clients = []

log.startLogging(sys.stdout)
reactor.listenTCP(9999, MyFactory(2))
reactor.run()
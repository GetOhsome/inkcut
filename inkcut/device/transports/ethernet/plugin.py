# -*- coding: utf-8 -*-
"""
Copyright (c) 2017-2019, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Jul 12, 2015

@author: jrm
"""
import serial
import traceback
from atom.atom import set_default
from atom.api import List, Instance, Enum, Bool, Int, Unicode
from inkcut.core.api import Plugin, Model, log
from inkcut.device.plugin import DeviceTransport
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.serialport import SerialPort
from serial.tools.list_ports import comports

from inkcut.device.transports.raw.plugin import RawFdTransport, RawFdProtocol
import socket


#: Reverse key values
SERIAL_PARITIES = {v: k for k, v in serial.PARITY_NAMES.items()}


class EthernetConfig(Model):
    port = Unicode().tag(config=True)
    ip = Unicode().tag(config=True)

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------

    def _default_ip(self):
        return "192.168.2.100"

    def _default_port(self):
        return "3333"


class EthernetTransport(DeviceTransport):
    config = Instance(EthernetConfig, ()).tag(config=True)
    connection = Instance(socket.socket)
    d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #: Whether a serial connection spools depends on the device (configuration)
    always_spools = set_default(False)

    def connect(self):
        print("SeroIP connected")
        print(self.config.ip)
        print(self.config.port)
        self.d.connect((self.config.ip, int(self.config.port)))
        self.connected = True

    def write(self, data):
        print("SeroIP printing " + data)
        self.d.send(data.encode())

    def disconnect(self):
        print("SeroIP disconnected")
        self.d.close()
        self.connected = False

        # if self.d:
        #     self.connection.close()

    def repr(self):
        return self.config.printer


class SerialPlugin(Plugin):
    """ Plugin for handling serial port communication

    """

    # -------------------------------------------------------------------------
    # SerialPlugin API
    # -------------------------------------------------------------------------

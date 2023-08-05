# modbus-tcp-server

[![PyPI](https://img.shields.io/pypi/pyversions/modbus-tcp-server.svg)](https://pypi.python.org/pypi/modbus-tcp-server)
[![PyPI version](https://badge.fury.io/py/modbus-tcp-server.svg)](https://badge.fury.io/py/modbus-tcp-server)
[![PyPI](https://img.shields.io/pypi/implementation/modbus-tcp-server.svg)](https://pypi.python.org/pypi/modbus-tcp-server)
[![Wheel](https://img.shields.io/pypi/wheel/modbus-tcp-server.svg)](https://pypi.org/project/modbus-tcp-server/)
[![License](https://img.shields.io/pypi/l/smok)](https://github.com/smok-serwis/modbus-tcp-server)

A thread-based MODBUS TCP server for testing purposes.

# Installation

Just type 

```bash
pip install modbus-tcp-server
```

And to run it

```bash
modbus-tcp-server 127.0.0.1 502
```

Port is optional, it will be assumed to be 502 by default.

Just run it without any arguments to see the command line.

If you want verbosity, you can drop `-v` or `-vv` after providing port number.
Note that in this case giving port number is mandatory.

# Limitations

It does only the commands related to reading and writing
analog inputs, discrete inputs, holding registers and coils,
so only commands 1-6 and 15-16 are supported.

Also, it spawns a thread per a client. This might be unacceptable to you,
however it can also with with gevent.

Client connections will be closed after 60 seconds of inactivity.

# Custom data provider

To implement a custom data provider, just extend
[BaseDataSource](modbus_tcp_server/data_source/base.py) 
to provide data of your choosing and launch it that way: 

```python
from modbus_tcp_server.network import ModbusTCPServer
from modbus_tcp_server.data_source import BaseDataSource

class CustomDB(BaseDataSource):
    ...

c_db = CustomDB()

at = ModbusTCPServer('0.0.0.0', 502, c_db).start()
```

Note that since everything is handled in a single thread, 
if your reads or writes take too long this will hang on them.
File a Issue if you've got a problem with that.

# Change log

## v0.6

* made logging received data log level debug
* socket will be opened with SO_REUSEADDR

## v0.4

* added automatic connection termination after 60 seconds of inactivity
* better error detection on connections
* bugfix: fixed CustomMODBUSError

## v0.3

* added `CustomMODBUSError`
* renamed `AcceptThread` to `ModbusTCPServer`

## v0.2

* added support for commands 15 and 16
* added exceptions `GatewayPathUnavailable` and
    `GatewayTargetDeviceFailedToRespond`

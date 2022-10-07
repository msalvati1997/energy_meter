from datetime import datetime
from threading import Thread
from socket import socket
import time
from multiprocessing import Process
import os
import json
import socket
import datetime
import sys
from virtualwatts.__main__ import run_virtualwatts, VirtualWattsConfigValidator


class MainProcess(Process):
    """
    Process to host VirtualWatts
    """
    def __init__(self):
        Process.__init__(self)

    def run(self):
        config = {'verbose': True,
                  "stream":True,
                  'input': {'puller_filedb':
                               { "type": "mongodb",
                                 "uri": "mongodb://127.0.0.1",
                                 "db": "powerapi",
                                 "collection": "smartwatts"
                                },
                            "puller_tcpdb": {
                                 "type" : "socket",
                                  "model": "ProcfsReport",
                                  "uri": "127.0.0.1",
                                   "port": 8080
                                 }
                  },
                  "output": {
                             "power_pusher": {
                              "type": "influxdb",
                              "model": "PowerReport",
                              "uri": "127.0.0.1",
                              "port": 8086,
                              "db": "powerapi_formula",
                              "collection": "prep"
                             }
                },
                  'delay-threshold': 500,
                  'sensor-reports-sampling-interval': datetime.timedelta(500)}
        # Next command is reached
        if not VirtualWattsConfigValidator.validate(config):
            sys.exit(-1)
        run_virtualwatts(config)


def main() :
    vw_pro = MainProcess()
    vw_pro.start()


if __name__ == "__main__":
    main()
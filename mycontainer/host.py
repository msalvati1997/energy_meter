from datetime import datetime
from threading import Thread
from socket import socket
import pymongo
import time
from multiprocessing import Process
import os
import json
import socket
import datetime
import sys
from virtualwatts.__main__ import run_virtualwatts, VirtualWattsConfigValidator



class FileThread(Thread):
    """
    Thread that open a virtual file and write a list of reports
    """

    def __init__(self, msg_list, filename):
        Thread.__init__(self)

        self.msg_list = msg_list
        self.filename = filename

    def run(self):
        time.sleep(0.5)
        for msg in self.msg_list:
            file_obj = open(self.filename, 'w')
            file_obj.write(json.dumps(msg))
            file_obj.close()
            time.sleep(0.5)

class MainProcess(Process):
    """
    Process to host VirtualWatts
    """
    def __init__(self,port):
        Process.__init__(self)
        self.port = port

    def run(self):
        config = {'verbose': True,
                  "stream":True,
                  'input': {'puller_filedb': {'type': 'filedb',
                                              'model': 'PowerReport',
                                              'filename': 'SW_output'},
                            'puller_tcpdb': {'type' : 'socket',
                                             'model': 'ProcfsReport',
                                             'uri': '127.0.0.1',
                                             'port': self.port}
                            },
                  'output': {'power_pusher': {'type': 'mongodb',
                                              'model': 'PowerReport',
                                              'uri': "mongodb://127.0.0.1",
                                              'db': "OUTPUT",
                                              'collection': "prep"}},
                  'delay-threshold': 500,
                  'sensor-reports-sampling-interval': datetime.timedelta(500)}
        # Next command is reached
        if not VirtualWattsConfigValidator.validate(config):
            sys.exit(-1)
        run_virtualwatts(config)
        
    
def test(unused_tcp_port, virtualwatts_power_timeline ):
    file_sensor = FileThread(virtualwatts_power_timeline, 'SW_output')

    vw_pro = MainProcess(unused_tcp_port)
    vw_pro.start()
    file_sensor.start()
    file_sensor.join()

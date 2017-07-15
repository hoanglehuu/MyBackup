


import telnetlib
import threading
import time, os, sys

PROMPT = ':~$'

class clTelnetConnect(threading.Thread):
    def __init__(self, num_of_cmds):
        super(clTelnetConnect, self).__init__()
        self.tn = None
        self.num_of_cmds = num_of_cmds
        self.f = self.login()

    def login(self):
        try:
            self.tn = telnetlib.Telnet('192.168.6.101')
            #self.tn.set_debuglevel(3)
            self.tn.read_until('login:')
            self.tn.write('clovis\r\n')
            self.tn.read_until('Password:')
            self.tn.write('clovis\r\n')
            self.tn.read_until(PROMPT)
            return 0
        except:
            return -1

    def run_cmd(self, cmd):
        try:
            self.tn.write('%s\r\n'%cmd)
            self.tn.read_until(PROMPT)
            print self.tn.read_very_lazy()
            return 0
        except Exception as ex:
            print ex
            return -1
        return 0

    def run(self):
        # Retry connect to telnetd
        if self.f != 0:
            self.f = self.login()
      
        for i in range(0, self.num_of_cmds):
            print "[%s] Run cmd [%d]!!!"%(self.getName(), i)
            loop = 0
            ret = self.run_cmd('ls -l /tmp')
            while (loop < 10 and ret == -1):
                ret = self.run_cmd('ls -l /tmp')
                loop = loop + 1

        self.tn.write('exit\r\n')
        #print self.tn.read_all()			
        self.tn.close()

threadlist = []
num_of_threads = 1
num_of_cmds = 1
start = time.time()

try:
    num_of_threads = int(sys.argv[1])
    num_of_cmds = int(sys.argv[2])
except:
    num_of_threads = 2
    num_of_cmds = 2

for x in range(num_of_threads):
    t = clTelnetConnect(num_of_cmds)
    threadlist.append(t)

for t in threadlist:
    t.start()

for t in threadlist:
    t.join()
    print "Thread " + t.name + " finished!"

finish = time.time()
interval = finish - start
print "Execution lasted for " + str(interval) + " seconds!"

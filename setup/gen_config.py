#!/usr/bin/env python

import os, sys, time, getopt
import pexpect
import getpass
import time
from string import Template
import argparse
import subprocess

DEFAULT_SECRET = 'secret'
NUM_SIP_CLIENTS = 20
USER_BASE=6000


'''
sip.conf Setup
[general]
tcpenable=yes
tcpbindaddr=0.0.0.0
'''
SIP_CONF_TPL='''[general](+)
tcpenable=yes                   ; Enable server for incoming TCP connections (default is no)
tcpbindaddr=0.0.0.0             ; IP address for TCP server to bind to (0.0.0.0 binds to all interfaces)
                                ; Optionally add a port number, 192.168.1.1:5062 (default is port 5060)
'''

AC_TPL="""[{user}](testcase1_tpl)
defaultuser={user}
secret={secret}
context = default
"""

DATA_SEQ_TPL="""{user1};{sipp_host};[authentication username={user1} password={secret}];{user2};
"""

DICT_CONF = dict()
DICT_CONF["dbport"]     = ''
DICT_CONF["dbname"]     = ''
DICT_CONF["dbuser"]     = ''
DICT_CONF["dbpass"]     = ''
DICT_CONF["userconf"]   = '''
; User template
;----------------------------------
[testcase1_tpl](!)
type = friend
canreinvite = no
host = dynamic
dtmfmode = rfc2833
callgroup = 1
pickupgroup = 1
disallow = all
allow = ulaw
allow = alaw
transport=tcp,udp
'''
DICT_CONF["extentions"] = ''
DICT_CONF["sipconf"] = ''

DICT_CONF["data"]       = '''SEQUENTIAL
#UAC1@IP1 -> UAC(n-1)@IP1
'''
DICT_CONF["query"] = ''

DICT_CONF["pjsua_account_udp"] = ''
DICT_CONF["pjsua_account_tcp"] = ''

PJSUA_ACCOUNT_TPL='''
--id sip:{user}@{ast_host}
--registrar sip:{ast_host};transport={transport}
--realm asterisk
--username {user}
--password {secret}
'''

CONFS = ["sip.conf.tpl","users.conf.tpl", "db.sql.tpl", "sipp/data.csv.tpl"]
CONFS_SPLIT = ["pjsua/pjsua_udp.conf.tpl", "pjsua/pjsua_tcp.conf.tpl"]

def formatUserName(namestr):
	return ''.join(namestr.split()).strip().lower()

'''
SIPp is simulating number of num_sip_clients/2 UACs, each one of them is making outgoing call. 
This scenario expects calls to be answered.
Call targets are number of 'num_sip_clients' other UACs remain configured to auto answer and play wav file (single pjsua instance with 'num_sip_clients'/2 remain accounts).

Example: num_sip_clients = 6 -> accounts: 6001,6002,6003,6004,6005,6006
SIPp (caller) <->   Asterisk     <-> pjsua (callee)
6001                  ||           6006
6002                  ||           6005
6003                  ||           6004
'''
def generate_config(args):

    num_sip_clients = NUM_SIP_CLIENTS

    #pjsua (callee) tcp configuration

    #pjsua (callee) tls configuration

    if args.num_sip_client != 0:
        if (args.num_sip_client%2) == 0:
            num_sip_clients = args.num_sip_client
        else:
            parser.print_help()
            exit(0)

    for i in range(0, int(num_sip_clients) + 1):
        DICT_CONF["userconf"] += AC_TPL.format(user=(USER_BASE+i), secret=DEFAULT_SECRET)


    PART_SPLIT=10
    iterator = 0

    for i in range(0, int(num_sip_clients)/2):
        # (caller)
        # SIPp is simulating num_sip_clients/2 UACs, each one of them is making outgoing call.
        DICT_CONF["data"] += DATA_SEQ_TPL.format(user1=(USER_BASE+i), user2=(USER_BASE+(num_sip_clients - i)), secret=DEFAULT_SECRET, sipp_host = args.sipp_host)

        for t in ('udp','tcp'):
            # udp,tcp,tls account
            DICT_CONF["pjsua_account_%s"%t] += PJSUA_ACCOUNT_TPL.format(user=(USER_BASE+(num_sip_clients - i)), secret=DEFAULT_SECRET, ast_host = DICT_CONF["ast_host"], transport=t)

            if (i < (int(num_sip_clients)/2 - 1)):
                DICT_CONF["pjsua_account_%s"%t] += '--next-account'

        # Because pjsua does not allow too much arguments (max=128), to work-around, do split file and run on each command
        if ((i+1)%PART_SPLIT) == 0:
            # Do write and empty dict
            for conf in CONFS_SPLIT:
                out = '.'.join(["%s_r%d"%(conf.split(".")[0], iterator)] + [conf.split(".")[1]])
                try:
                    example_conf = Template(open(conf).read().strip())
                    open(out, "w").write(example_conf.safe_substitute(DICT_CONF))
                except Exception, e:
                    print e
                    pass

            # New file no
            iterator+=1
            for t in ('udp','tcp'):
                # udp,tcp,tls account
                DICT_CONF["pjsua_account_%s"%t] = ''

    DICT_CONF["sipconf"] += Template(SIP_CONF_TPL).safe_substitute(DICT_CONF)
    for conf in CONFS:
        out = '.'.join(conf.split(".")[0:-1])
        try:
            example_conf = Template(open(conf).read().strip())
            open(out, "w").write(example_conf.safe_substitute(DICT_CONF))
        except Exception, e:
            print e
            pass

    # Do write data remain if avaiable (udp,tcp)
    if len(DICT_CONF["pjsua_account_udp"]) > 0:
        for conf in CONFS_SPLIT:
            out = '.'.join(["%s_r%d"%(conf.split(".")[0], iterator)] + [conf.split(".")[1]])
            try:
                example_conf = Template(open(conf).read().strip())
                open(out, "w").write(example_conf.safe_substitute(DICT_CONF))
            except Exception, e:
                print e
                pass

    #Import DB
    cmd='psql --host $ast_host --port $dbport --username $dbuser $dbname -f db.sql'
    cmd=Template(cmd).safe_substitute(DICT_CONF)

    print "Database importing for host %s, cmd=[%s]:"%(DICT_CONF["ast_host"],cmd)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    print p.communicate()[0]
    pass

global args
global parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--dbport", dest="dbport", default = '9999', help='Port to connect to postgres')
    parser.add_argument("--dbname", dest="dbname", default = 'data_parse', help='DB name')
    parser.add_argument("--dbuser", dest="dbuser", default = 'postgres', help='User owner of database')
    parser.add_argument("--dbpass", dest="dbpass", default = '')

    parser.add_argument("--ast_host", dest="ast_host", required=True, help='IP address of Asterisk Server')
    parser.add_argument("--sipp_host", dest="sipp_host", required=True, help='IP address of UAC register (caller)')
    parser.add_argument("--pjsua_host", dest="pjsua_host", required=True, help='IP address of UAC register (callee)')

    parser.add_argument("--num_sip_client", dest="num_sip_client", type=int, default = 20, help='Number of sip users using realtime, using even number (2,4,6...)')

    args = parser.parse_args()

    DICT_CONF["ast_host"] = args.ast_host
    DICT_CONF["sipp_host"] = args.sipp_host
    DICT_CONF["pjsua_host"] = args.pjsua_host

    DICT_CONF["dbport"] = args.dbport
    DICT_CONF["dbname"] = args.dbname
    DICT_CONF["dbuser"] = args.dbuser
    DICT_CONF["dbpass"] = args.dbpass

    generate_config(args)

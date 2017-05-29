
#!/usr/bin/env python

import os, sys, time, getopt

LIST_CMDS='''dundi query 08:00:27:D1:84:75@priv
dundi query 08:00:27:F9:44:3B@priv
dundi query FF:FF:FF:FF:FF:FF@priv
dundi query 00:00:00:00:00:00@priv
dundi precache 6000@priv
dundi precache 6020@priv
dundi precache 6001@priv
dundi precache 6019@priv
dundi precache 6002@priv
dundi precache 6018@priv
dundi precache 6003@priv
dundi precache 6017@priv
dundi precache 6004@priv
dundi precache 6016@priv
dundi precache 6005@priv
dundi precache 6015@priv
dundi precache 6006@priv
dundi precache 6014@priv
dundi precache 6007@priv
dundi precache 6013@priv
dundi precache 6008@priv
dundi precache 6012@priv
dundi precache 6009@priv
dundi precache 6011@priv

dundi lookup 6000@priv
dundi lookup 6020@priv
dundi lookup 6001@priv
dundi lookup 6019@priv
dundi lookup 6002@priv
dundi lookup 6018@priv
dundi lookup 6003@priv
dundi lookup 6017@priv
dundi lookup 6004@priv
dundi lookup 6016@priv
dundi lookup 6005@priv
dundi lookup 6015@priv
dundi lookup 6006@priv
dundi lookup 6014@priv
dundi lookup 6007@priv
dundi lookup 6013@priv
dundi lookup 6008@priv
dundi lookup 6012@priv
dundi lookup 6009@priv
dundi lookup 6011@priv
'''

for cmd in LIST_CMDS.split("\n"):
    if len(cmd.strip()) > 0:
        os.system("asterisk -rx \"%s\""%cmd.strip())
        time.sleep(1)

sys.exit(0)


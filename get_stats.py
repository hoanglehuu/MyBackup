#!/usr/bin/env python

import os, sys, time, getopt
import time
from string import Template
import argparse
import subprocess

HEADER = [("Function","# Execution","# TAT (secs)")]
REPORTING = dict()

def print_table(table, fcsv):
    rows = HEADER + table

    table.sort(key=lambda r: r[0])

    if fcsv == True:
        print ",".join(HEADER[0])
        for line in table:
            print ",".join(line)
    else:
        col_width = [max(len(x) for x in col) for col in zip(*rows)]
        strformat = ['{0:-<%d}'%col_width[i] for i, x in enumerate(('','',''))]

        print "+ " + " + ".join(strformat[i].format(x) for i, x in enumerate(('','',''))) + " +"
        #Print header row
        print "+ " + " + ".join("{0:{1}}".format(x, col_width[i]) for i, x in enumerate(HEADER[0])) + " +"
        print "+ " + " + ".join(strformat[i].format(x) for i, x in enumerate(('','',''))) + " +"
        for line in table:
            print "| " + " | ".join("{0:{1}}".format(x, col_width[i]) for i, x in enumerate(line)) + " |"

        print "+ " + " + ".join(strformat[i].format(x) for i, x in enumerate(('','',''))) + " +"

def process_time(ret):
    time = 0.0000000
    for p in ret.split(","):
        if "(sec)" in p:
            time = p.replace("(sec)","").strip()
            break;
        
    return float(time)

def get_stat(lkfile, lkfunc, results):
    count_exec = 0
    total_tat = 0;
    for ret in results:
        if ',%s,'%lkfunc in ret and lkfile in ret:
            count_exec += 1
            total_tat += process_time(ret)

    REPORTING["%s:%s"%(lkfile,lkfunc)] = [count_exec, total_tat]


def process_func_list(func_list):
    results = []
    curfile = None
    for line in func_list:
        if ":" in line:
            #Handle key file
            key = line.split(":")[0].strip()
            func = line.split(":")[1].strip()
            curfile = key
            if len(func) > 0:
                results.append(":".join([curfile,func]))
        else:
            func = None
            for p in line.split():
                if "(" in p:
                    func = p.split("(")[0].replace("*",'')
                    break
            if func:
                results.append(":".join([curfile,func]))
    return results

def get_stats(func_list_file_path, log_file_path, fcsv):
    try:
        func_list = open(func_list_file_path).read().strip().split("\n")
        results = open(log_file_path).read().strip().split("\n")
    except Exception, e:
        print "Loading file error!", e
        sys.exit(1)

    func_list = process_func_list(func_list)

    for func in func_list:
        lkfile, lkfunc = tuple(func.split(":"))
        get_stat(lkfile, lkfunc, results)


    table = ([(str(x), "%s"%REPORTING[x][0], "%s"%"{0:.6f}".format(REPORTING[x][1])) for x in REPORTING])
    print_table(table, fcsv)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--func_list", dest="func_list", required=True, help='Function list file')
    parser.add_argument("--log_file", dest="log_file", required=True, help='Asterisk\'s message log file')
    parser.add_argument("--csv", dest="csv", help='Output format', action='store_true', default=False)

    args = parser.parse_args()

    get_stats(args.func_list, args.log_file, args.csv)

#!/usr/bin/env python
"""Build a new database

"""

import fattybugs
import os
import sys
import getopt

def usage():
    usage_str="""USAGE:
Build a database and write the config file
    build_db.py [-c CONFIGFILE] DB_FILE
        *NOTE* Default CONFIGFILE is "$HOME/.fattybugs

Build a database and don't write the config file:
    build_db.py -d DB_FILE
"""
    print(usage_str)



def main(argv):
    """Parse the arguments, then build the database"""
    configfile=None
    write_config=True
    
    try:
        opts,args=getopt.getopt(argv,"hdc:")
    except getopt.GetoptError():
        usage()
        sys.exit(2)

    for opt,arg in opts:
        if opt=="-h":
            usage()
            sys.exit()
        elif opt in ("-c"):
            configfile=arg
        elif opt in ("-d"):
            write_config=False
        
    if (not write_config) and (configfile):
        usage()
        sys.exit(2)
    
    if not args:
        usage()
        sys.exit(2)
    if len(args) > 1 :
        usage()
        sys.exit(2)

    if write_config and not configfile:
        configfile=fattybugs.default_configfile()

    fattybugs.build_db(args[0],write_configs=write_config,configfile=configfile)

if __name__=="__main__":
    main(sys.argv[1:])

#!/usr/bin/env python
"""List all bugs in the bug database


"""

import fattybugs
import os
import sys
import getopt


def usage():
    usage_str="""
USAGE:
List bugs in the default database, as specified in the configuration file:
    list_bugs.py [-c CONFIGFILE]
        Default CONFIGFILE is either $HOME/.fattybugs or $USERPROFILE/.fattybugs

List bugs in an alternate database file:
    list_bugs.py DB_FILE

"""
    print(usage_str)



def main(argv):
    """Parse the arguments, then build the database"""
    configfile=None
    db_file=None
    try:
        opts,args=getopt.getopt(argv,"hc:")
    except getopt.GetoptError():
        usage()
        sys.exit(2)

    for opt,arg in opts:
        if opt=="-h":
            usage()
            sys.exit()
        elif opt in ("-c"):
            configfile=arg
        
    if len(args) > 0:
        db_file=args[0]
    else:
        db_file=fattybugs.default_bug_db()
    bdb=fattybugs.BugDB(db_file)
    bdb.list_bugs()

if __name__=="__main__":
    main(sys.argv[1:])




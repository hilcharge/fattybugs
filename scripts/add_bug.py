#!/usr/bin/env python
"""Add a bug to the database


"""

import fattybugs
import os
import sys
import getopt


def usage():
    usage_str="""
USAGE:
Add bugs in the default database, as specified in the configuration file:
    add_bug.py [-c CONFIGFILE] [ BUG_DATA ]
        Default CONFIGFILE is either $HOME/.fattybugs or $USERPROFILE/.fattybugs

Add bugs in an alternate database file:
    add_bug.py  [ BUG_DATA ] DB_FILE

BUG_DATA:
    -r REPRODUCTION_STEPS
    -a ASSIGNED_TO
    -o OBSERVED_BEHVAIOR
    -e EXPECTED_BEHAVIOR
    -n BUG_NAME
"""
    print(usage_str)

def main(argv):
    """Parse the arguments, then build the database"""
    configfile=None
    db_file=None
    new_data={
        "reproduction_steps" : None,
        "expected_behavior" : None,
        "observed_behavior" :None,
        "assigned_to":None,
        "bug_name": None,
        }

    try:
        opts,args=getopt.getopt(argv,"hc:o:r:e:a:n:")
    except getopt.GetoptError():
        usage()
        sys.exit(2)

    for opt,arg in opts:
        if opt=="-h":
            usage()
            sys.exit()
        elif opt in ("-c"):
            configfile=arg
        elif opt in ("-a"):
            new_data["assigned_to"]=arg
        elif opt in ("-e"):
            new_data["expected_behavior"]=arg
        elif opt in ("-o"):
            new_data["observed_behavior"]=arg
        elif opt in ("-r"):
            new_data["reproduction_steps"]=arg
        elif opt in ("-n"):
            new_data["bug_name"]=arg
        
    if len(args) > 0:
        db_file=args[0]
    else:
        db_file=fattybugs.default_bug_db()
    bdb=fattybugs.BugDB(db_file)

    bdb.new_bug(**new_data)

if __name__=="__main__":
    main(sys.argv[1:])




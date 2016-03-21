#!/usr/bin/env python
"""Add a bug to the database


"""

import fattybugs
import os
import sys
import getopt
import re

def usage():
    usage_str="""
USAGE:
Fix a bug in the default database, as specified in the configuration file:
    add_bug.py [-c CONFIGFILE] [ BUG_NAME ]
        Default CONFIGFILE is either $HOME/.fattybugs or $USERPROFILE/.fattybugs

Add bugs in an alternate database file:
    fix_bug.py [ -d DATABASE ] [ BUG_NAME ]

"""
    print(usage_str)

def main(argv):
    """Parse the arguments, then build the database"""
    configfile=None
    db_file=None
    bug_name=None

    try:
        opts,args=getopt.getopt(argv,"hc:d:")
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
            db_file=arg

    if len(args) > 0:
        bug_name=args[0]
    if not db_file:
        if not configfile:
            configfile=fattybugs.default_configfile()
        db_file=fattybugs.default_bug_db(configfile)
        
    bdb=fattybugs.BugDB(db_file)
    existing_bugs=list(bdb.bugs(name_only=True))
    if bug_name and (bug_name not in existing_bugs):
        print("ERROR: The specified bug {} is not an active bug".format(bug_name),file=sys.stderr)
        sys.exit(2)
        
    if not bug_name:
        while bug_name not in existing_bugs:            
            print("*************")
            print("Active bugs:")
            for i,b in enumerate(existing_bugs):
                print(i+1,") ",b)
            print("*************")
            print("Selection options:")
            print("   # : Select the bug number #")
            print("   #h : More details about bug number #")
            print("   a : List details of all bugs")
            print("   q : Quit ")
            resp=input("Please enter your selection (#,#h,a)> ")
            try:
                bug_name=existing_bugs[int(resp)-1]
            except IndexError:
                print("ERROR: Invalid selection",file=sys.stderr)
            except (ValueError,TypeError):
                m=re.match(r"(\d+)+h$",resp)
                if m:                    
                    num=int(m.groups(1)[0])
                    bdb.bug_details_display(bug_name=existing_bugs[int(num)-1])
                elif resp.lower()=="a":
                    bdb.list_bugs()
                elif resp.lower()=="q":
                    sys.exit()
                
                else:
                    print("ERROR: Invalid selection",file=sys.stderr)
    bdb.fix_bug(bug_name=bug_name)

if __name__=="__main__":
    main(sys.argv[1:])




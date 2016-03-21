"""Module for dealing with a very simple sqlite bug-tracking database

The database is just a table with seven columns as follows:

* The five JOEL test columns:
    * reproduction_steps
    * expected_behavior
    * observed_behavior
    * assigned_to
    * fixed
* Identifier:
    * bug_name
* The two following date columns, which are handled automatically
    * date_created
    * date_fixed


NO OTHER COLUMNS should be relied on. This is made as a basic way to level up in the JOEL test for software development.

If you want to add more columns to the table, that is fine, but do not rely on this module.

Ok, now let's look at how to use this

Detailed usage:
================

Make a bug database
-------------
   
    > from fattybugs import fattybugs
    > db_file="/path/to/shared/bug_db.db
    > bdb=fattybugs.build_db(db_file,write_config=True)
    # Setting write_config=True will cause a ".fattybugs" file to bewritten in your $HOME directory

Create a connection
------------------

Connect to the default BugDB as follows:

    > bdb=fattybugs.default_BugDB()

This will create a connection to the bug database defined in your .fattybugs

If you have some different bug database, you can use the following sequence:

    > bugdb=fattybugs.BugDB(DB_FILENAME)

DB_FILENAME can be retrieved from your configuration file if you wish:

    > DB_FILENAME=fattybugs.default_bug_db()


List all the unfixed bugs
-----------

Use the list_bugs method

    > bugdb.list_bugs()


Create a new bug via prompts
----------------------------
 
    > bugdb.new_bug()


You can include values in the input to this method to avoid prompting

    > bugdb.new_bug(reproduction_steps="...",expected_behavior="...",observed_behavior="...",assigned_to="...",bug_name="...")

`reproduction_steps` can be a list or text.


Fix a bug
--------------

    > bugdb.fix_bug([bug_name="..."])

If no bug_name is input, then you can choose from the list


Retrieve details about a bug
-------------------------

    > bugdb.bug_data(bug_name="my-bug-name")

OR
 
    > bugdb.bug_data(bug_id=2)
 

Dipslay details about a bug
----------------------

    > bugdb.bug_details_display(bug_name="my-bug-name")

OR
 
    > bugdb.bug_details_display(bug_id=2) 



Reassign a bug
-----------------

    > bugdb.reassign("New Person",bug_id=2)    


"""

import os

import sqlite3
import logging
import datetime
import configparser

class FattyException(Exception):
    pass

class BugDB:    

    #define the columns
    STEPS_COLUMN="reproduction_steps"
    XB_COLUMN="expected_behavior"
    OB_COLUMN="observed_behavior"
    ASS_COLUMN="assigned_to"
    FIXED_COLUMN="fixed"
    NAME_COLUMN="bug_name"
    CREATED_DATE_COLUMN="date_created"
    DATE_FIXED_COLUMN="date_fixed"

    BUG_COLUMN_LIST=(    STEPS_COLUMN,
                         XB_COLUMN,
                         OB_COLUMN,
                         ASS_COLUMN,
                         NAME_COLUMN,
    )                              

    BUG_TABLE="bugs"
    
    def __init__(self,filename,**kwargs):
        self.cxn=sqlite3.connect(filename,detect_types=sqlite3.PARSE_DECLTYPES)
        self.cxn.row_factory=sqlite3.Row
        self.filename=filename

    def bugs(self,active_only=True):
        """Return all bug information, in form of a list of dictionaries. 
If active_only is is set to False, return a list of all previous bugs"""
        q="SELECT {},{},{},{},{},{},{} FROM {} ".format(
            BugDB.NAME_COLUMN,
            BugDB.STEPS_COLUMN,
            BugDB.XB_COLUMN,
            BugDB.OB_COLUMN,
            BugDB.ASS_COLUMN,
            BugDB.CREATED_DATE_COLUMN,
            BugDB.FIXED_COLUMN,
            BugDB.BUG_TABLE,

        )
        params=[]
        if active_only:
            q+="""
        WHERE {} IS NOT ?
""".format(BugDB.FIXED_COLUMN)
        
            params.append(1)
        q+=" ORDER BY ROWID"
        with self.cxn:
            cur=self.cxn.cursor()
            for row in cur.execute(q,params):                
                name=row["bug_name"]
                bug={}
                for k in row.keys():
                    bug[k]=row[k]
                yield bug

    def list_bugs(self,active_only=True):
        """list all active bugs, or all bugs if active_only is set  to False"""
        for bug in self.bugs(active_only=active_only):
            print("*******************")
            name=bug["bug_name"]
            for k in bug.keys():
                
                print(name+"\t"+k+"\t"+str(bug[k]).replace("\n","  ;;  "))

            print("*******************")                    
                                        
    def new_bug(self,**kwargs):
        """register a new bug, return the ROWID

        Keyword args:
        the column names of the database and their values
        """
        params={}

        try:
            force=kwargs["force"]
        except KeyError:
            force=False

        multilines=[BugDB.STEPS_COLUMN,BugDB.XB_COLUMN,BugDB.OB_COLUMN]
        existing_bugs=[ b[BugDB.NAME_COLUMN] for b in self.bugs(active_only=False)]
        for column_name in BugDB.BUG_COLUMN_LIST:            
            try:
                params[column_name]=kwargs[column_name]
            except KeyError:
                if not force:
                    if column_name in multilines:
                        params[column_name]=multiline_input("Enter value for {}".format(column_name))
                    else:
                        if column_name==BugDB.NAME_COLUMN:
                            params[column_name]=input("Enter value for {}:> ".format(column_name))
                            while params[column_name] in existing_bugs:
                                print("KABLAMMO! That name is chosen already")
                                params[column_name]=input("Enter value for {}:> ".format(column_name))

        if not len(params):
            logging.error("No data given about bug, not inserting it")
            return None
        else:
            #prepare the date data
            params[BugDB.CREATED_DATE_COLUMN]=datetime.datetime.now()
        
        params[BugDB.FIXED_COLUMN]=0
        q="""INSERT INTO {} ({})
        VALUES ({})""".format(self.BUG_TABLE,",".join(params.keys()),",".join([":{}".format(k) for k in params.keys()]))        

        cur=self.cxn.cursor()
        cur.execute(q,params)
        
        self.cxn.commit()

        return cur.lastrowid

    def fix_bug(self,**kwargs):
        """update the database to specify that the bug is fixed,

        Keyword args:
        bug_name ORbug_id

        If no keyword argument is given, then you will be prompted to choose one       

        """

        params={}

        if "bug_id" in kwargs:
            params["ROWID"]=kwargs["bug_id"]
        if self.NAME_COLUMN in kwargs:
            params[self.NAME_COLUMN]=kwargs[self.NAME_COLUMN]
        

        q="""UPDATE {} SET {} WHERE {}""".format(
            self.BUG_TABLE,
            ",".join(["{}=1".format(self.FIXED_COLUMN),"{}=:datefixed".format(self.DATE_FIXED_COLUMN)]),
            " AND ".join(["{}=:{}".format(k,k) for k in params])
        )
        params["datefixed"]=datetime.datetime.now()

        cur=self.cxn.cursor()
        cur.execute(q,params)
        self.cxn.commit()

        
        
    # def bug_details(self,**kwargs):
    #     """retrieve a data structure specifying details about a bug

    #     Keyword args:
    #     bug_name or id

    #     If no keyword argument is given, then you will be prompted to choose one               
    #     """
    #     params={}
    #     bug_dets={}

    #     if "rowid" in kwargs:
    #         params["ROWID"]=kwargs["rowid"]
    #     if self.NAME_COLUMN in kwargs:
    #         params[self.NAME_COLUMN]=kwargs[self.NAME_COLUMN]

    #     q="SELECT {},{},{},{},{},{},{} FROM {} WHERE {}".format(                               
    #         BugDB.NAME_COLUMN,
    #         BugDB.STEPS_COLUMN,
    #         BugDB.XB_COLUMN,
    #         BugDB.OB_COLUMN,
    #         BugDB.ASS_COLUMN,
    #         BugDB.CREATED_DATE_COLUMN,
    #         BugDB.FIXED_COLUMN,
    #         BugDB.BUG_TABLE,
    #         " AND ".join(["{}=:{}".format(p,p) for p in params])
    #     )
    #     row={}
    #     with self.cxn:
    #         cur=self.cxn.cursor()
    #         cur.execute(q,params)
    #         row=cur.fetchone()
            
    #     return {k:row[k] for k in row.keys()}

    def bug_data(self,**kwargs):
        """retrieve a data structure specifying details about a bug
        returns the data as a dictionary

        Keyword args:
        bug_name or bug_id

        For more fine tuned selection, consider using the `bugs` method to retrieve all data, and filter from there
        """
        params={}
        if "bug_id" in kwargs:
            params["rowid"]=kwargs["bug_id"]
        elif self.NAME_COLUMN in kwargs:
            params[self.NAME_COLUMN]=kwargs["name"]
        else:
            raise FattyException("You must supply either a bug_id or a bug_name as a keyword argument. Not provided in kwargs: "+str(kwargs))

        q="SELECT {},{},{},{},{},{},{} FROM {} WHERE {}".format(
            BugDB.NAME_COLUMN,
            BugDB.STEPS_COLUMN,
            BugDB.XB_COLUMN,
            BugDB.OB_COLUMN,
            BugDB.ASS_COLUMN,
            BugDB.CREATED_DATE_COLUMN,
            BugDB.FIXED_COLUMN,
            BugDB.BUG_TABLE,
            " AND ".join(["{}=:{}".format(p,p) for p in params])
            )
        row=None
        with self.cxn:
            cur=self.cxn.cursor()
            cur.execute(q,params)
            row=cur.fetchone()
            return row
    def reassign(self,assign_to,**kwargs):
        """Reassign the bug of the given name or bug_id to the `assigned_to`
"""
        q="UPDATE bugs SET assigned_to=? WHERE "
        params=[assign_to,]
        if "bug_id" in kwargs:
            q += "ROWID=?"
            params.append(kwargs["bug_id"])
        elif self.NAME_COLUMN in kwargs:
            q += BugDB.NAME_COLUMN+"=?"
            params.append(kwargs["bug_name"])
        else:
            raise FattyException("You must supply either a bug_id or a bug_name as a keyword argument. Not provided in kwargs: "+str(kwargs))
        
        cur=self.cxn.cursor()
        cur.execute(q,params)
        self.cxn.commit()
        
    def bug_details_display(self,**kwargs):
        """retrieve a data structure specifying details about a bug

        Keyword args:
        bug_name or bug_id
        
        """
        row=self.bug_data(**kwargs)
        print("*******************")
        for k in row.keys():
            print(k,":", str(row[k]).replace("\n","\n{}>  ".format(k)))
        print("*******************")                    
                        
def build_db(db_filename,write_configs=False,configfile=None):
    """Build a bug database at the given db_filename location
If write_configs is set to True, write the config file, with section "bugs", and option "db_file"
"""

    conn = sqlite3.connect(db_filename)
    cur=conn.cursor()
    sql="""
CREATE TABLE bugs(
reproduction_steps text,
expected_behavior text, observed_behavior text,
assigned_to text,
fixed INTEGER,
date_created timestamp,
date_fixed timestamp,
bug_name text);
"""
    cur.executescript(sql)
    conn.commit()

    conn.close()

    if not os.path.isfile(db_filename):        
        raise FattyException("Unable to create database file")
                      
    configs=configparser.ConfigParser()
    configs.add_section("bug_db")

    configs.set("bug_db","db_file",db_filename)
    if write_configs:
        write_config(configs,configfile)

def write_config(configs,configfile=None):
    """Write a config file. using the default $HOME/.fattybugs filename if none is present"""

    if not configfile:
        configfile=_default_configfile()

    with open(configfile,"w") as cfh:
        configs.write(cfh)

def _default_configfile():
    """return the default config filename, which is either $HOME/.fattybugs, or $USERPROFILE/.fattybugs

raises FattyException if no 
"""
    dirname=None
    if os.getenv("HOME"):
        dirname=os.getenv("HOME")
    elif os.getenv("USERPROFILE"):
        dirname=os.getenv("USERPROFILE")

    else:
        raise FattyException("No HOME or USERPROFILE variable set, unable to determine default config file")

    return os.path.join(dirname,".fattybugs")
    
def default_configs():
    """Return the default configparser object"""
    configs=configparser.ConfigParser()
    configs.read(_default_configfile())
    
    return configs
                              
    
def default_bug_db():
    """return the filename of the default bug database, this is based on relative directories"""

    configs=default_configs()

    db_file=os.path.normpath(configs.get("bug_db","db_file"))
    return db_file

def default_BugDB():
    db_file=default_bug_db()
    
    return BugDB(db_file)

def multiline_input(prompt):
    """Prompt for multiline input"""

    lines=[]
    print(prompt+" : (input will end after entering a blank line)")
    while True:
        line=input()
        if not line.strip():
            break
        else:
            lines.append(line)

    return "\n".join(lines)
        
        

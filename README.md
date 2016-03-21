# fattybugs
basic python module and scripts for working with sqlite3 bug tracking database. This is a really easy way to level up on the JOEL, because it has the 5 reuired fields and only requires having python.


Install
--------

python setup.py install



Summary
--------

Module for dealing with a very simple sqlite bug-tracking database

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
